/*****************************************************************************/
/* VISION BOX FIRMWARE - CORNFLEIS TEAM */
/*****************************************************************************/

#include <math.h>
#include "pwm.h"


void BSP_PWM_Init()
{
    // Configure timer used by PWM
    const ledc_timer_config_t pwm_timer = {
        .duty_resolution = PWM_RESOLUTION,
        .freq_hz = PWM_FREQ_HZ,
        .speed_mode = PWM_SPEED_MODE,
        .timer_num = PWM_TIMER,
        .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&pwm_timer);

    // Configure LED Controller (PWM) channel being used,
    // initially setting duty cycle to 0
    ledc_channel_config_t pwm_channel = {
        .channel = PWM_CHANNEL,
        .gpio_num = PWM_OUTPUT_GPIO,
        .duty = 0,
        .speed_mode = PWM_SPEED_MODE,
        .timer_sel = PWM_TIMER,
        .hpoint = 0
    };
    ledc_channel_config(&pwm_channel);

    return;
}

void BSP_PWM_SetDuty(uint8_t percentage)
{
    assert(percentage <= 100);

    // Convert input percentage to a duty value from
    // 0 to 2^PWM_RESOLUTION (example 0 - 1023 with 10-bit resolution)
    uint32_t duty_cycle = (percentage * (uint32_t)pow(2,PWM_RESOLUTION))/100;

    ledc_set_duty(PWM_SPEED_MODE, PWM_CHANNEL, duty_cycle);
    ledc_update_duty(PWM_SPEED_MODE, PWM_CHANNEL);
    return;
}

void BSP_PWM_SetFrequency(uint32_t frequency_hz)
{
    ledc_set_freq(PWM_SPEED_MODE, PWM_TIMER, frequency_hz);
    return;
}