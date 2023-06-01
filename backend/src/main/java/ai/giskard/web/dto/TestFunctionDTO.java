package ai.giskard.web.dto;

import com.dataiku.j2ts.annotations.UIModel;
import com.fasterxml.jackson.annotation.JsonAlias;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.util.List;
import java.util.UUID;

@Data
@UIModel
public class TestFunctionDTO {
    @NotNull
    private UUID uuid;
    @NotBlank
    private String name;
    @NotBlank
    @JsonAlias("display_name")
    private String displayName;
    private Integer version;
    private String module;
    private String doc;
    @JsonAlias("module_doc")
    private String moduleDoc;
    @NotBlank
    private String code;
    private List<@NotBlank String> tags;
    private List<TestFunctionArgumentDTO> args;
}
