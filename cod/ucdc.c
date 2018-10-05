#include "ucdc.h"
#include "usbd_cdc.h"

extern void MX_USB_DEVICE_Init(void) ;

static UCDC_CFG cfg ;

static USBD_CDC_LineCodingTypeDef LineCoding = {
    115200, /* baud rate*/
    0x00,   /* stop bits-1*/
    0x00,   /* parity - none*/
    0x08    /* nb. of bits 8*/
} ;


extern USBD_HandleTypeDef hUsbDeviceFS ;

/* Private functions ---------------------------------------------------------*/
/**
  * @brief  Initializes the CDC media low layer over the FS USB IP
  * @retval USBD_OK if all operations are OK else USBD_FAIL
  */

static int8_t CDC_Init_FS(void)
{
    cfg.cb_ini() ;

    return (USBD_OK) ;
}

/**
  * @brief  DeInitializes the CDC media low layer
  * @retval USBD_OK if all operations are OK else USBD_FAIL
  */
static int8_t CDC_DeInit_FS(void)
{
    return (USBD_OK) ;
}

/**
  * @brief  Manage the CDC class requests
  * @param  cmd: Command code
  * @param  pbuf: Buffer containing command data (request parameters)
  * @param  length: Number of data to be sent (in bytes)
  * @retval Result of the operation: USBD_OK if all operations are OK else USBD_FAIL
  */
static int8_t CDC_Control_FS(uint8_t cmd, uint8_t* pbuf, uint16_t length)
{
    switch (cmd) {
    case CDC_SEND_ENCAPSULATED_COMMAND:
        break ;

    case CDC_GET_ENCAPSULATED_RESPONSE:
        break ;

    case CDC_SET_COMM_FEATURE:
        break ;

    case CDC_GET_COMM_FEATURE:
        break ;

    case CDC_CLEAR_COMM_FEATURE:
        break ;

    /*******************************************************************************/
    /* Line Coding Structure                                                       */
    /*-----------------------------------------------------------------------------*/
    /* Offset | Field       | Size | Value  | Description                          */
    /* 0      | dwDTERate   |   4  | Number |Data terminal rate, in bits per second*/
    /* 4      | bCharFormat |   1  | Number | Stop bits                            */
    /*                                        0 - 1 Stop bit                       */
    /*                                        1 - 1.5 Stop bits                    */
    /*                                        2 - 2 Stop bits                      */
    /* 5      | bParityType |  1   | Number | Parity                               */
    /*                                        0 - None                             */
    /*                                        1 - Odd                              */
    /*                                        2 - Even                             */
    /*                                        3 - Mark                             */
    /*                                        4 - Space                            */
    /* 6      | bDataBits  |   1   | Number Data bits (5, 6, 7, 8 or 16).          */
    /*******************************************************************************/
    case CDC_SET_LINE_CODING:
        LineCoding.bitrate = (uint32_t)(pbuf[0] | (pbuf[1] << 8) | \
                                        (pbuf[2] << 16) | (pbuf[3] << 24)) ;
        LineCoding.format = pbuf[4] ;
        LineCoding.paritytype = pbuf[5] ;
        LineCoding.datatype = pbuf[6] ;

        break ;

    case CDC_GET_LINE_CODING:
        pbuf[0] = (uint8_t)(LineCoding.bitrate) ;
        pbuf[1] = (uint8_t)(LineCoding.bitrate >> 8) ;
        pbuf[2] = (uint8_t)(LineCoding.bitrate >> 16) ;
        pbuf[3] = (uint8_t)(LineCoding.bitrate >> 24) ;
        pbuf[4] = LineCoding.format ;
        pbuf[5] = LineCoding.paritytype ;
        pbuf[6] = LineCoding.datatype ;

        break ;

    case CDC_SET_CONTROL_LINE_STATE:
        break ;

    case CDC_SEND_BREAK:
        break ;

    default:
        break ;
    }

    return (USBD_OK) ;
}

/**
  * @brief  Data received over USB OUT endpoint are sent over CDC interface
  *         through this function.
  *
  *         @note
  *         This function will block any OUT packet reception on USB endpoint
  *         untill exiting this function. If you exit this function before transfer
  *         is complete on CDC interface (ie. using DMA controller) it will result
  *         in receiving more data while previous ones are still not sent.
  *
  * @param  Buf: Buffer of data to be received
  * @param  Len: Number of data received (in bytes)
  * @retval Result of the operation: USBD_OK if all operations are OK else USBD_FAIL
  */
static int8_t CDC_Receive_FS(uint8_t* Buf, uint32_t *Len)
{
	cfg.cb_rx(Buf, *Len) ;
//    USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]) ;
//    USBD_CDC_ReceivePacket(&hUsbDeviceFS) ;
    return (USBD_OK) ;
}

static void cb_fineTx(void)
{
	cfg.cb_tx() ;
}

USBD_CDC_ItfTypeDef USBD_Interface_fops_FS = {
    CDC_Init_FS,
    CDC_DeInit_FS,
    CDC_Control_FS,
    CDC_Receive_FS,
    cb_fineTx
} ;


/**
  * @brief  UCDC_tx
  *         Data to send over USB IN endpoint are sent over CDC interface
  *         through this function.
  *         @note
  *
  *
  * @param  Buf: Buffer of data to be sent
  * @param  Len: Number of data to be sent (in bytes)
  * @retval USBD_OK if all operations are OK else USBD_FAIL or USBD_BUSY
  */

bool UCDC_tx(void * Buf, uint16_t Len)
{
    bool esito = false ;
    USBD_CDC_HandleTypeDef *hcdc =
        (USBD_CDC_HandleTypeDef*)hUsbDeviceFS.pClassData ;
    if (hcdc->TxState != 0) {
    }
    else {
        USBD_CDC_SetTxBuffer(&hUsbDeviceFS, Buf, Len) ;
        esito = USBD_OK == USBD_CDC_TransmitPacket(&hUsbDeviceFS) ;
    }

    return esito ;
}

void UCDC_rx(void * buf, uint16_t dim)
{
    USBD_CDC_SetRxBuffer(&hUsbDeviceFS, (uint8_t *) buf) ;
    USBD_CDC_ReceivePacket(&hUsbDeviceFS) ;
}

bool UCDC_ini(const UCDC_CFG * pCFG)
{
	cfg = *pCFG ;

    MX_USB_DEVICE_Init() ;

    return true ;
}
