dependencies {
    developmentOnly("org.springframework.boot:spring-boot-devtools:${springBootVersion}")
}

val profiles = "dev"
if (project.hasProperty("no-liquibase")) {
    profiles += ",no-liquibase"
}
if (project.hasProperty("tls")) {
    profiles += ",tls"
}

springBoot {
    buildInfo {
        properties {
            time = null
        }
    }
}

bootRun {
    args = listOf()
}


processResources {
    inputs.property("version", version)
    inputs.property("springProfiles", profiles)
    filesMatching("**/application.yml") {
        filter {
            it.replace("#project.version#", version)
        }
    }
}

