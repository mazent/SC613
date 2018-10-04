#define STAMPA_DBG
#include "includimi.h"

#include "main.h"
#include "stm32f0xx_hal.h"
#include "usb_device.h"

extern void app(void) ;

DMA_HandleTypeDef hdma_adc ;

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct ;
    RCC_ClkInitTypeDef RCC_ClkInitStruct ;
    RCC_PeriphCLKInitTypeDef PeriphClkInit ;

    /**Initializes the CPU, AHB and APB busses clocks
    */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI14 |
                                       RCC_OSCILLATORTYPE_HSE ;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON ;
    RCC_OscInitStruct.HSI14State = RCC_HSI14_ON ;
    RCC_OscInitStruct.HSI14CalibrationValue = 16 ;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON ;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE ;
    RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL4 ;
    RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1 ;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        _Error_Handler(__FILE__, __LINE__) ;
    }

    /**Initializes the CPU, AHB and APB busses clocks
    */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                  | RCC_CLOCKTYPE_PCLK1 ;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK ;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1 ;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1 ;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK) {
        _Error_Handler(__FILE__, __LINE__) ;
    }

    PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USB ;
    PeriphClkInit.UsbClockSelection = RCC_USBCLKSOURCE_PLL ;

    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK) {
        _Error_Handler(__FILE__, __LINE__) ;
    }

//    /**Configure the Systick interrupt time
//    */
//    HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq() / 1000) ;
//
//    /**Configure the Systick
//    */
//    HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK) ;
//
//    /* SysTick_IRQn interrupt configuration */
//    HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0) ;
}



/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{
    /* DMA controller clock enable */
    __HAL_RCC_DMA1_CLK_ENABLE() ;

    /* DMA interrupt init */
    /* DMA1_Channel1_IRQn interrupt configuration */
    HAL_NVIC_SetPriority(DMA1_Channel1_IRQn, 0, 0) ;
    HAL_NVIC_EnableIRQ(DMA1_Channel1_IRQn) ;
}

/** Configure pins as
        * Analog
        * Input
        * Output
        * EVENT_OUT
        * EXTI
*/
static void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct ;

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOF_CLK_ENABLE() ;
    __HAL_RCC_GPIOA_CLK_ENABLE() ;
    __HAL_RCC_GPIOB_CLK_ENABLE() ;

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(GPIOB,
                      RES1_Pin | RES2_Pin | RES3_Pin | RES_Pin
                      | RES4_Pin | VERDE_Pin | ROSSO_Pin | BUFFER_Pin,
                      GPIO_PIN_RESET) ;

    /*Configure GPIO pins : RES1_Pin RES2_Pin RES3_Pin RES_Pin
                             RES4_Pin VERDE_Pin ROSSO_Pin BUFFER_Pin */
    GPIO_InitStruct.Pin = RES1_Pin | RES2_Pin | RES3_Pin | RES_Pin
                          | RES4_Pin | VERDE_Pin | ROSSO_Pin | BUFFER_Pin ;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP ;
    GPIO_InitStruct.Pull = GPIO_NOPULL ;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW ;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct) ;

    /*Configure GPIO pin : USB_IN_Pin */
    GPIO_InitStruct.Pin = USB_IN_Pin ;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT ;
    GPIO_InitStruct.Pull = GPIO_NOPULL ;
    HAL_GPIO_Init(USB_IN_GPIO_Port, &GPIO_InitStruct) ;
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  file: The file name as string.
  * @param  line: The line in file as a number.
  * @retval None
  */
void _Error_Handler(char *file, int line)
{
#ifdef NDEBUG
	NVIC_SystemReset() ;
#else
	DBG_PRINTF("ERROR_HANDLER: %s %" PRIu32 "\r\n", file, line) ;
	__BKPT(0) ;
#endif
}

#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{
    DBG_PRINTF("ASSERT_FAILED: %s %" PRIu32 "\r\n", file, line) ;

    BPOINT ;
}

#endif /* USE_FULL_ASSERT */

int main(void)
{
//#ifndef NDEBUG
//	HAL_DBGMCU_EnableDBGStopMode() ;
//	HAL_DBGMCU_EnableDBGStandbyMode() ;
//#endif

    /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
    HAL_Init() ;

    /* Configure the system clock */
    SystemClock_Config() ;

    /* Initialize all configured peripherals */
    MX_GPIO_Init() ;
    MX_DMA_Init() ;

    MX_USB_DEVICE_Init() ;

    app() ;
}
