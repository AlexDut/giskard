package ai.giskard.service.ee;

import ai.giskard.config.ApplicationProperties;
import ai.giskard.service.FileLocationService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.bouncycastle.crypto.params.Ed25519PublicKeyParameters;
import org.bouncycastle.crypto.signers.Ed25519Signer;
import org.bouncycastle.util.encoders.Hex;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.nio.file.Files;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.util.Base64;

@Service
@RequiredArgsConstructor
public class LicenseService {

    private final Logger log = LoggerFactory.getLogger(LicenseService.class);

    private final FileLocationService fileLocationService;

    private final ApplicationProperties properties;

    private License currentLicense;

    /**
     * On service init, load the stored license if it exists
     * Also initialize default license (for now)
     */
    @PostConstruct
    public void init() throws IOException {
        if (currentLicense == null) {
            if (Files.exists(fileLocationService.licensePath())) {
                String licenseFile = Files.readString(fileLocationService.licensePath());
                initializeLicense(licenseFile);
            } else {
                // The default license has "active" set to false -> it will go back to the setup page
                currentLicense = new License();
            }
        }
    }

    /**
     * Shorthand for LicenseService.getCurrentLicense().hasFeature(flag) since it's a very common call
     *
     * @param flag FeatureFlag we want to check
     * @return whether the provided flag is enabled or not
     */
    public boolean hasFeature(FeatureFlag flag) {
        return this.getCurrentLicense().hasFeature(flag);
    }

    public synchronized License getCurrentLicense() {
        return currentLicense;
    }

    /**
     * Takes a license file content, parses it, validates that it is a proper license.
     * If it's a real license, saves it in giskard home and updates available feature flags
     *
     * @param licenseFile
     */
    public synchronized void uploadLicense(String licenseFile) throws IOException {
        initializeLicense(licenseFile);
        Files.write(fileLocationService.licensePath(), licenseFile.getBytes());
    }

    private void initializeLicense(String lic) throws IOException {
        // 1. Remove start/end decorators
        String encodedPayload = lic.replaceAll(
            "^-----BEGIN LICENSE FILE-----\\n|" +
                "\\n|" +
                "-----END LICENSE FILE-----\\n$",
            "");

        // 2. Decode base64 => json
        byte[] payloadBytes = Base64.getDecoder().decode(encodedPayload);
        String payload = new String(payloadBytes);
        ObjectMapper mapper = new ObjectMapper();
        JsonNode payloadJson = mapper.readTree(payload);

        // 3. Parse Json
        String encodedData = payloadJson.get("enc").asText();
        String encodedSig = payloadJson.get("sig").asText();
        String algorithm = payloadJson.get("alg").asText();

        if (!"base64+ed25519".equals(algorithm)) {
            throw new LicenseValidationException();
        }

        // 4. Decode signing bytes and use signature to validate
        if (!verifySignature(encodedData, encodedSig)) {
            throw new LicenseValidationException();
        }

        // 5. Decode license and parse it into a License object
        String decodedLicense = new String(Base64.getDecoder().decode(encodedData));
        JsonNode licenseJson = mapper.readTree(decodedLicense);

        JsonNode meta = licenseJson.get("meta");
        if (!verifyExpired(meta)) {
            throw new LicenseExpiredException();
        }

        License newLicense = License.fromJson(licenseJson);
        if (!newLicense.isActive()) {
            throw new LicenseValidationException();
        }

        log.info("License file loaded. Plan: {}", newLicense.getPlanName());

        this.currentLicense = newLicense;
    }


    private boolean verifySignature(String encodedData, String encodedSig) {
        byte[] publicKeyBytes = Hex.decode(properties.getLicensePublicKey());
        byte[] signatureBytes = Base64.getDecoder().decode(encodedSig);
        byte[] encDataBytes = String.format("license/%s", encodedData).getBytes();

        Ed25519PublicKeyParameters verifierParams = new Ed25519PublicKeyParameters(publicKeyBytes, 0);
        Ed25519Signer verifier = new Ed25519Signer();

        verifier.init(false, verifierParams);
        verifier.update(encDataBytes, 0, encDataBytes.length);

        return verifier.verifySignature(signatureBytes);
    }

    private boolean verifyExpired(JsonNode licenseMetadata) {
        Instant now = Instant.now();
        Instant issued = ZonedDateTime.parse(licenseMetadata.get("issued").asText()).toInstant();
        Instant expiry = ZonedDateTime.parse(licenseMetadata.get("expiry").asText()).toInstant();

        return issued.isBefore(now) && expiry.isAfter(now);
    }
}
