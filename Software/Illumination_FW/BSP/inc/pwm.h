/*****************************************************************************/
/* VISION BOX PC APPLICATION - CORNFLEIS TEAM */
/*****************************************************************************/

#ifndef PWM_H
#define PWM_H

/******************************** INCLUDES ***********************************/
#include "driver/ledc.h"

/********************************* DEFINES ***********************************/
#define PWM_SPEED_MODE        LEDC_LOW_SPEED_MODE   // Mode selection
#define PWM_TIMER             LEDC_TIMER_1          // Low speed timer selected for PWM

#define PWM_OUTPUT_GPIO       (18)                  // GPIO Pin 18 selected as output
#define PWM_CHANNEL           LEDC_CHANNEL_0

#define PWM_RESOLUTION        LEDC_TIMER_8_BIT      // Choose 8 bit resolution (0-255)
#define PWM_FREQ_HZ           (500)                 // 500 Hz PWM frequency

/*************************** FUNCTION PROTOTYPES *****************************/

/**
 * @brief PWM Init: Initializes all required hardware peripherals (GPIO and
 *        timers) with the parameters specified in the defines of pwm.h
 * @param none
 * @return void
 */
void BSP_PWM_Init();

/**
 * @brief Sets PWM duty cycle in respect to input percentage and 
 *        configured resolution
 * @param uint8_t percentage - Input value from 0 to 100% 
 * @return void
 */
void BSP_PWM_SetDuty(uint8_t percentage);

/**
 * @brief Sets PWM frequency in Herz
 * @param uint32_t frequency_hz - Integer with frequency in Herz
 * @return void
 */
void BSP_PWM_SetFrequency(uint32_t frequency_hz);


#endif // PWM_H