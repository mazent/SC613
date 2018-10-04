#define STAMPA_DBG
#include "includimi.h"
#include "soc.h"
#include "buzzer.h"

#define ROSSO_MILLI		500

static void led_rosso(void)
{
	HAL_GPIO_TogglePin(ROSSO_GPIO_Port, ROSSO_Pin) ;

	timer_start(TIM_LEDR, ROSSO_MILLI) ;
}

#define VERDE_MILLI		600

static void led_verde(void)
{
	HAL_GPIO_TogglePin(VERDE_GPIO_Port, VERDE_Pin) ;

	timer_start(TIM_LEDV, VERDE_MILLI) ;
}

#define CICA_A_MILLI		100
#define CICA_S_MILLI		400

static bool cica = false ;

static void cicalino(void)
{
	if (cica) {
		BUZZER_Freq(0) ;
		timer_start(TIM_CICA, CICA_S_MILLI) ;
	}
	else {
		BUZZER_Freq(4000) ;
		timer_start(TIM_CICA, CICA_A_MILLI) ;
	}
	cica = !cica ;
}

void app(void)
{
    {
    	uint32_t w0 = HAL_GetUIDw0() ;
    	uint32_t w1 = HAL_GetUIDw1() ;
    	uint32_t w2 = HAL_GetUIDw2() ;

    	DBG_PRINTF("scaldabagno %08X%08X%08X\n", w0, w1, w2) ;
    }

    SOC_ini() ;

    timer_setcb(TIM_LEDR, led_rosso) ;
    timer_start(TIM_LEDR, ROSSO_MILLI) ;

    timer_setcb(TIM_LEDV, led_verde) ;
    timer_start(TIM_LEDV, VERDE_MILLI) ;

    CONTROLLA( BUZZER_Iniz() ) ;
    cica = false ;
//    timer_setcb(TIM_CICA, cicalino) ;
//    timer_start(TIM_CICA, 1) ;

    while (true) {
    	SOC_run() ;

    	HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI) ;
    }
}
