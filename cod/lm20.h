#ifndef LM20_H_
#define LM20_H_

// 130 gradi
#define LM20_MAX	13000

// -55 gradi
#define LM20_MIN	-5500

// In caso di errore gx100 conterra' LM20_MIN o LM20_MAX
bool LM20_temp(uint16_t adc, int16_t * gx100) ;

#endif
