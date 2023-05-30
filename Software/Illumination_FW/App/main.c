#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "pwm.h"

void app_main(void)
{
    BSP_PWM_Init();
    BSP_PWM_SetDuty(70);

    while(1)
    {
        vTaskDelay(1000/portTICK_PERIOD_MS);
        printf("PWM set to 70 percent\n");
    }
}
