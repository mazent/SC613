#ifndef INCLUDIMI_H_
#define INCLUDIMI_H_

// Questi vanno inclusi sempre
// ==========================================

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
// Per le PRIu32 ecc
#include <inttypes.h>

#include "stm32f0xx_hal.h"
#include "utili.h"

// Scheda
// ==========================================

//#define PIN_ALT(a, b)		(((volatile GPIO_TypeDef *) a)->BSRR = b)
//#define PIN_BAS(a, b)		(((volatile GPIO_TypeDef *) a)->BSRR = (b << 16))
//#define PIN_VAL(a, b)		(((volatile GPIO_TypeDef *) a)->IDR & b)

static inline void MZ_GPIO_DeInit(GPIO_TypeDef * GPIOx, uint32_t GPIO_Pin)
{
    GPIO_InitTypeDef git = {
        .Mode = GPIO_MODE_ANALOG,
        .Pull = GPIO_NOPULL,
        .Pin = GPIO_Pin
    } ;

    // Questo riporta allo stato di reset
    HAL_GPIO_DeInit(GPIOx, GPIO_Pin) ;

    // Per il consumo
    HAL_GPIO_Init(GPIOx, &git) ;
}

/*
 * Macro da impostare
 * 		*) Tipo di processore: STM32F072xB
 * 		*) USE_HAL_DRIVER  
 *      *) NDEBUG/USE_FULL_ASSERT: in release/debug 
 */

#endif

