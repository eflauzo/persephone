#ifndef SIREN_H
#define SIREN_H

#include <stdint.h>

struct SirenArbId {
   uint8_t priority;
   uint8_t function_code;
   uint8_t data_page;
   uint8_t reserved;
   uint8_t destination;
   uint8_t source_address;
};

uint32_t SirenArbId_encode(struct SirenArbId*);
void SirenArbId_decode(struct SirenArbId*, uint32_t);

struct SirenSprinkle_Command_t{
    uint8_t Sprinkler4;
    uint8_t Sprinkler2;
    uint8_t Sprinkler3;
    uint8_t Sprinkler1;
};

/* Encode SirenSprinkle_Command_t into CAN frame */
void SirenSprinkle_Command_encode(struct SirenSprinkle_Command_t*, uint8_t data[]);

/* Decode SirenSprinkle_Command_t from CAN frame */
void SirenSprinkle_Command_decode(struct SirenSprinkle_Command_t*, uint8_t data[]);
struct SirenPing_t{
    uint16_t torque;
};

/* Encode SirenPing_t into CAN frame */
void SirenPing_encode(struct SirenPing_t*, uint8_t data[]);

/* Decode SirenPing_t from CAN frame */
void SirenPing_decode(struct SirenPing_t*, uint8_t data[]);
struct SirenSprinklerStatus_t{
    uint8_t Sprinkler4;
    uint8_t Sprinkler2;
    uint8_t Sprinkler3;
    uint8_t Sprinkler1;
};

/* Encode SirenSprinklerStatus_t into CAN frame */
void SirenSprinklerStatus_encode(struct SirenSprinklerStatus_t*, uint8_t data[]);

/* Decode SirenSprinklerStatus_t from CAN frame */
void SirenSprinklerStatus_decode(struct SirenSprinklerStatus_t*, uint8_t data[]);

struct SirenDispatcher_t{
   void *user_data;
   void (*on_Sprinkle_Command_ptr)(struct SirenDispatcher_t*, uint32_t arb_id, struct SirenSprinkle_Command_t *msg);
   void (*on_Ping_ptr)(struct SirenDispatcher_t*, uint32_t arb_id, struct SirenPing_t *msg);
   void (*on_SprinklerStatus_ptr)(struct SirenDispatcher_t*, uint32_t arb_id, struct SirenSprinklerStatus_t *msg);
};

void Siren_init(struct SirenDispatcher_t*);
void Siren_dispatch(struct SirenDispatcher_t*, uint32_t arb_id, uint8_t data[]);


/* initialize Sprinkle_Command message with message specific ID fields */
void SirenSprinkle_Command_init(struct SirenArbId* arb_id, struct SirenSprinkle_Command_t* data);

/* initialize Ping message with message specific ID fields */
void SirenPing_init(struct SirenArbId* arb_id, struct SirenPing_t* data);

/* initialize SprinklerStatus message with message specific ID fields */
void SirenSprinklerStatus_init(struct SirenArbId* arb_id, struct SirenSprinklerStatus_t* data);

#endif