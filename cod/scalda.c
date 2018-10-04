#define STAMPA_DBG
#include "includimi.h"
#include "scalda.h"

bool SCALDA_ini(void)
{
	// cfr MX_GPIO_Init

	HAL_GPIO_WritePin(BUFFER_GPIO_Port, BUFFER_Pin, GPIO_PIN_SET) ;

	return true ;
}

void SCALDA_fin(void)
{
	HAL_GPIO_WritePin(BUFFER_GPIO_Port, BUFFER_Pin, GPIO_PIN_RESET) ;
}

void SCALDA_1(bool si)
{
	HAL_GPIO_WritePin(RES1_GPIO_Port, RES1_Pin, si ? GPIO_PIN_SET : GPIO_PIN_RESET) ;
}

void SCALDA_2(bool si)
{
	HAL_GPIO_WritePin(RES2_GPIO_Port, RES2_Pin, si ? GPIO_PIN_SET : GPIO_PIN_RESET) ;
}

void SCALDA_3(bool si)
{
	HAL_GPIO_WritePin(RES3_GPIO_Port, RES3_Pin, si ? GPIO_PIN_SET : GPIO_PIN_RESET) ;
}

void SCALDA_4(bool si)
{
	HAL_GPIO_WritePin(RES4_GPIO_Port, RES4_Pin, si ? GPIO_PIN_SET : GPIO_PIN_RESET) ;
}

void SCALDA_x(bool si)
{
	HAL_GPIO_WritePin(RES_GPIO_Port, RES_Pin, si ? GPIO_PIN_SET : GPIO_PIN_RESET) ;
}

