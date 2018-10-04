#define STAMPA_DBG
#include "includimi.h"
#include "buzzer.h"

extern void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim) ;

#define PWM_FREQ_MAX    1000000
#define FREQ_TYP        4000

static TIM_HandleTypeDef htim17 = {
	.State = HAL_TIM_STATE_RESET,

	.Instance = TIM17,

	.Init = {
		.CounterMode = TIM_COUNTERMODE_UP,
		.ClockDivision = TIM_CLOCKDIVISION_DIV1,
		.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE
	}
} ;

static bool iniz = false ;
static uint32_t freqCorr ;

static void ctrl_uscita(TIM_HandleTypeDef * timer, uint32_t canale, bool abil)
{
	if (abil) {
        __HAL_TIM_SET_COUNTER(timer, 0) ;
        HAL_TIMEx_PWMN_Start(timer, canale) ;
	}
	else
		HAL_TIMEx_PWMN_Stop(timer, canale) ;
}

static void cambia_freq(TIM_HandleTypeDef * timer, uint32_t fmax, uint32_t hz)
{
	uint32_t tmp = (fmax / hz) - 1 ;

	timer->Instance->ARR = tmp ;

	// Duty-cycle del 50%
	timer->Instance->CCR1 = tmp >> 1 ;

	//timer->Instance->EGR = TIM_EGR_UG ;
}

static void cambia_duty(TIM_HandleTypeDef * timer, uint32_t perc)
{
	uint32_t tmp = timer->Instance->ARR + 1 ;

	if (perc >= 100) {
		// 100 %
	}
	else {
		tmp *= perc ;
		tmp /= 100 ;
		tmp -= 1 ;
	}

	timer->Instance->CCR1 = tmp ;
}


bool BUZZER_Iniz(void)
{
    assert(!iniz) ;

    if (!iniz) {
        uint32_t clock = HAL_RCC_GetPCLK1Freq() ;

        htim17.Init.Prescaler = (clock / PWM_FREQ_MAX) - 1 ;
        htim17.Init.Period = (PWM_FREQ_MAX / FREQ_TYP) - 1 ;
        freqCorr = FREQ_TYP ;

        do {
        	// MX_TIM17_Init
            if (HAL_TIM_Base_Init(&htim17) != HAL_OK) {
                DBG_ERR ;
                break ;
            }

            if (HAL_TIM_PWM_Init(&htim17) != HAL_OK) {
                DBG_ERR ;
                break ;
            }

            TIM_OC_InitTypeDef sConfigOC = {
        		.OCMode = TIM_OCMODE_PWM1,

        		// duty-cicle 50%
        		.Pulse = htim17.Init.Period >> 1,

        		.OCPolarity = TIM_OCPOLARITY_HIGH,
        		.OCNPolarity = TIM_OCNPOLARITY_HIGH,
        		.OCFastMode = TIM_OCFAST_DISABLE,
        		.OCIdleState = TIM_OCIDLESTATE_RESET,
        		.OCNIdleState = TIM_OCNIDLESTATE_RESET
            } ;
            if (HAL_TIM_PWM_ConfigChannel(&htim17, &sConfigOC,
                                          TIM_CHANNEL_1) != HAL_OK) {
                DBG_ERR ;
                break ;
            }

            TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {
            	    .OffStateRunMode = TIM_OSSR_DISABLE,
            	    .OffStateIDLEMode = TIM_OSSI_DISABLE,
            	    .LockLevel = TIM_LOCKLEVEL_OFF,
            	    .DeadTime = 0,
            	    .BreakState = TIM_BREAK_DISABLE,
            	    .BreakPolarity = TIM_BREAKPOLARITY_HIGH,
            	    .AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE,
            } ;

            if (HAL_TIMEx_ConfigBreakDeadTime(&htim17,
                                              &sBreakDeadTimeConfig) != HAL_OK) {
                DBG_ERR ;
                break ;
            }

            HAL_TIM_MspPostInit(&htim17) ;

            iniz = true ;
        } while (false) ;
    }

    return iniz ;
}

void BUZZER_Fine(void)
{
	assert(iniz) ;

	if (iniz) {
		HAL_TIM_PWM_DeInit(&htim17) ;

	    iniz = false ;
	}
}

void BUZZER_Freq(int hz)
{
	assert(iniz) ;

	if (!iniz) {
	}
	else if (htim17.State != HAL_TIM_STATE_RESET) {
		ctrl_uscita(&htim17, TIM_CHANNEL_1, false) ;

        if (0 == hz) {
        	// Ottimo
        }
        else if (hz == freqCorr) {
        	// Buono
        	ctrl_uscita(&htim17, TIM_CHANNEL_1, true) ;
        }
        else {
        	cambia_freq(&htim17, PWM_FREQ_MAX, hz) ;
        	ctrl_uscita(&htim17, TIM_CHANNEL_1, true) ;
        }
    }
}

