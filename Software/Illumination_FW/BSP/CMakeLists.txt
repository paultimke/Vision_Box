set(SOURCES src/pwm.c)

idf_component_register(SRCS ${SOURCES}
                        INCLUDE_DIRS . inc
                        REQUIRES driver)