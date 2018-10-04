#define STAMPA_DBG
#include "includimi.h"
#include "temp.h"
#include "lm20.h"

static ADC_HandleTypeDef hadc = {
	.State = HAL_ADC_STATE_RESET,

	.Instance = ADC1,

	.Init = {
			.ClockPrescaler = ADC_CLOCK_ASYNC_DIV1,
			.Resolution = ADC_RESOLUTION_12B,
			.DataAlign = ADC_DATAALIGN_RIGHT,
			.ScanConvMode = ADC_SCAN_DIRECTION_FORWARD,
			.EOCSelection = ADC_EOC_SEQ_CONV,
			.LowPowerAutoWait = DISABLE,
			.LowPowerAutoPowerOff = DISABLE,
			.ContinuousConvMode = DISABLE,
			.DiscontinuousConvMode = DISABLE,
			.ExternalTrigConv = ADC_SOFTWARE_START,
			.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE,
			.DMAContinuousRequests = DISABLE,
			.Overrun = ADC_OVR_DATA_PRESERVED
	}
} ;

static bool ini = false ;

static enum {
	ADC_ATTESA,
	ADC_FINE,
	ADC_ERR
} stt_conv ;

#define ADC_CAMP_TEMP1		0
#define ADC_CAMP_TEMP2		1
#define ADC_CAMP_TEMP3		2
#define ADC_CAMP_TEMP4		3
#define ADC_CAMP_TEMPI		4
#define ADC_CAMP_VREFI		5
#define ADC_CAMP_MAX  		6

/* Value of analog voltage supply Vdda (unit: mV) */
#define VDDA_APPLI       ((uint32_t) 3300)
/* Max digital value with a full range of 12 bits */
#define FULL_SCALE       ((uint32_t) 4095)

#define TEMP30_CAL_ADDR   ((uint16_t*) ((uint32_t) 0x1FFFF7B8)) /* Internal temperature sensor, parameter TS_CAL1: TS ADC raw data acquired at a temperature of 110 DegC (+-5 DegC), VDDA = 3.3 V (+-10 mV). */
#define TEMP110_CAL_ADDR  ((uint16_t*) ((uint32_t) 0x1FFFF7C2)) /* Internal temperature sensor, parameter TS_CAL2: TS ADC raw data acquired at a temperature of  30 DegC (+-5 DegC), VDDA = 3.3 V (+-10 mV). */
#define VDDA_TEMP_CAL                  ((uint32_t) 3300)        /* Vdda value with which temperature sensor has been calibrated in production (+-10 mV). */


#define COMPUTATION_TEMPERATURE_TEMP30_TEMP110(TS_ADC_DATA)     \
  (((( ((int32_t)((TS_ADC_DATA * VDDA_APPLI) / VDDA_TEMP_CAL)   \
        - (int32_t) *TEMP30_CAL_ADDR)                           \
     ) * (int32_t)(110 - 30)                                    \
    ) / (int32_t)(*TEMP110_CAL_ADDR - *TEMP30_CAL_ADDR)         \
   ) + 30                                                       \
  )

/* Internal temperature sensor, parameter VREFINT_CAL: Raw data acquired at a temperature of 30 DegC (+-5 DegC), VDDA = 3.3 V (+-10 mV). */
/* This calibration parameter is intended to calculate the actual VDDA from Vrefint ADC measurement. */
#define VREFINT_CAL       ((uint16_t *) ((uint32_t) 0x1FFFF7BA))

/*
           3300 * VREFINT_CAL
	Vdda = ------------------
	          VREFINT_DATA

	        Vdda * adc    3300 * VREFINT_CAL * adc
	Vabs = ------------ = ------------------------
		    FULL_SCALE    VREFINT_DATA * FULL_SCALE
*/

static int32_t abs_volt(uint16_t adc, uint16_t vref)
{
	int32_t vrefint = *VREFINT_CAL ;
	int32_t num = 3300 * vrefint * adc ;
	int32_t den = FULL_SCALE * vref ;

	return num / den ;
}

static int32_t abs_adc(uint16_t adc, uint16_t vref)
{
	int32_t vrefint = *VREFINT_CAL ;
	int32_t num = vrefint * adc ;
	int32_t den = vref ;

	return num / den ;
}

static int16_t temp_int(uint16_t adc, uint16_t vref)
{
	int32_t val = abs_adc(adc, vref) ;
	int32_t t30 = *TEMP30_CAL_ADDR ;
	int32_t t110 = *TEMP110_CAL_ADDR ;
	int32_t num = (11000 - 3000) * (val - t30) ;
	int32_t den = t110 - t30 ;

	return 3000 + num / den ;
}

static int16_t temp_est(uint16_t adc, uint16_t vref)
{
	int32_t val = abs_adc(adc, vref) ;
	int16_t temp ;
#ifdef DBG_ABIL
	if ( !LM20_temp(val, &temp) ) {
		DBG_ERR ;
	}
#else
	(void) LM20_temp(val, &temp) ;
#endif

	return temp ;
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef * hadc)
{
	INUTILE(hadc) ;

	stt_conv = ADC_FINE ;
}

void HAL_ADC_ErrorCallback(ADC_HandleTypeDef *hadc)
{
	INUTILE(hadc) ;

	stt_conv = ADC_ERR ;
}

bool TEMP_iniz(void)
{
	do {
		if (ini)
			break ;

		// MX_ADC_Init

	    /**Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)*/
	    if (HAL_ADC_Init(&hadc) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    ADC_ChannelConfTypeDef sConfig = {
			.Rank = ADC_RANK_CHANNEL_NUMBER,
			.SamplingTime = ADC_SAMPLETIME_239CYCLES_5
	    } ;

	    sConfig.Channel = ADC_CHANNEL_0 ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    sConfig.Channel = ADC_CHANNEL_1 ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    sConfig.Channel = ADC_CHANNEL_2 ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    sConfig.Channel = ADC_CHANNEL_3 ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    sConfig.Channel = ADC_CHANNEL_TEMPSENSOR ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    /**Configure for the selected ADC regular channel to be converted.*/
	    sConfig.Channel = ADC_CHANNEL_VREFINT ;
	    if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK) {
	        DBG_ERR ;
	        break ;
	    }

	    ini = true ;
	} while (false) ;

	return ini ;
}

void TEMP_fine(void)
{
	HAL_ADC_DeInit(&hadc) ;
	ini = false ;
}

bool TEMP_val(S_TEMP * t)
{
	bool esito = false ;

	do {
		if (!ini) {
			DBG_ERR ;
			break ;
		}

		if (NULL == t) {
			DBG_ERR ;
			break ;
		}

		// Campionamento lento: ricalibro ogni volta
		if (HAL_ADCEx_Calibration_Start(&hadc) != HAL_OK) {
			DBG_ERR ;
			break ;
		}

		uint16_t camp[ADC_CAMP_MAX] ;
		stt_conv = ADC_ATTESA ;
		if (HAL_OK != HAL_ADC_Start_DMA(&hadc, (uint32_t *)camp, ADC_CAMP_MAX)) {
			DBG_ERR ;
			break ;
		}

		while (ADC_ATTESA == stt_conv)
			HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI) ;

		if (ADC_FINE == stt_conv) {
			t->temp1 = temp_est(camp[ADC_CAMP_TEMP1], camp[ADC_CAMP_VREFI]) ;
			t->temp2 = temp_est(camp[ADC_CAMP_TEMP2], camp[ADC_CAMP_VREFI]) ;
			t->temp3 = temp_est(camp[ADC_CAMP_TEMP3], camp[ADC_CAMP_VREFI]) ;
			t->temp4 = temp_est(camp[ADC_CAMP_TEMP4], camp[ADC_CAMP_VREFI]) ;

			t->temp = temp_int(camp[ADC_CAMP_TEMPI], camp[ADC_CAMP_VREFI]) ;

			esito = true ;
		}
		else {
			DBG_ERR ;
		}

	} while (false) ;

	HAL_ADC_Stop_DMA(&hadc) ;

	return esito ;
}
