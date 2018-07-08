#include "siren.h"
#include <stddef.h>
uint32_t SirenArbId_encode(struct SirenArbId* handle){
    uint32_t result = 0x0;
    result |= (uint32_t)(0x7 & handle->priority) << 26;
    result |= (uint32_t)(0xff & handle->function_code) << 16;
    result |= (uint32_t)(0x1 & handle->data_page) << 24;
    result |= (uint32_t)(0x1 & handle->reserved) << 25;
    result |= (uint32_t)(0xff & handle->destination) << 8;
    result |= (uint32_t)(0xff & handle->source_address) << 0;
    return result;
}

void SirenArbId_decode(struct SirenArbId* handle, uint32_t arbid){
    handle->priority = ((arbid >> 26) & 0x7);
    handle->function_code = ((arbid >> 16) & 0xff);
    handle->data_page = ((arbid >> 24) & 0x1);
    handle->reserved = ((arbid >> 25) & 0x1);
    handle->destination = ((arbid >> 8) & 0xff);
    handle->source_address = ((arbid >> 0) & 0xff);
}

void SirenSprinkle_Command_encode(struct SirenSprinkle_Command_t* handle, uint8_t data[]) {
    data[0] = 0x00;
    data[1] = 0x00;
    data[2] = 0x00;
    data[3] = 0x00;
    data[4] = 0x00;
    data[5] = 0x00;
    data[6] = 0x00;
    data[7] = 0x00;
    // serializing Sprinkler4
    unsigned long Sprinkler4_tmp = (unsigned long)((handle->Sprinkler4 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler4_tmp << 3) & 0b1000);
    Sprinkler4_tmp >>= 1;
    // serializing Sprinkler2
    unsigned long Sprinkler2_tmp = (unsigned long)((handle->Sprinkler2 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler2_tmp << 1) & 0b10);
    Sprinkler2_tmp >>= 1;
    // serializing Sprinkler3
    unsigned long Sprinkler3_tmp = (unsigned long)((handle->Sprinkler3 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler3_tmp << 2) & 0b100);
    Sprinkler3_tmp >>= 1;
    // serializing Sprinkler1
    unsigned long Sprinkler1_tmp = (unsigned long)((handle->Sprinkler1 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler1_tmp << 0) & 0b1);
    Sprinkler1_tmp >>= 1;
}

void SirenSprinkle_Command_decode(struct SirenSprinkle_Command_t* handle, uint8_t data[]) {
    uint8_t byte_i;
    // deserializing Sprinkler4
    unsigned long Sprinkler4_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 3;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler4_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler4 = Sprinkler4_tmp * (1) + (0);
    
    // deserializing Sprinkler2
    unsigned long Sprinkler2_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 1;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler2_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler2 = Sprinkler2_tmp * (1) + (0);
    
    // deserializing Sprinkler3
    unsigned long Sprinkler3_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 2;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler3_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler3 = Sprinkler3_tmp * (1) + (0);
    
    // deserializing Sprinkler1
    unsigned long Sprinkler1_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 0;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler1_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler1 = Sprinkler1_tmp * (1) + (0);
    
}

void SirenPing_encode(struct SirenPing_t* handle, uint8_t data[]) {
    data[0] = 0x00;
    data[1] = 0x00;
    data[2] = 0x00;
    data[3] = 0x00;
    data[4] = 0x00;
    data[5] = 0x00;
    data[6] = 0x00;
    data[7] = 0x00;
    // serializing torque
    unsigned long torque_tmp = (unsigned long)((handle->torque - (0)) / 1);
    data[0] = data[0] | ((torque_tmp << 0) & 0b11111111);
    torque_tmp >>= 8;
    data[1] = data[1] | ((torque_tmp << 0) & 0b11111111);
    torque_tmp >>= 8;
}

void SirenPing_decode(struct SirenPing_t* handle, uint8_t data[]) {
    uint8_t byte_i;
    // deserializing torque
    unsigned long torque_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 0;
    byte_i &= 0xff; /* Masking out bits 0b11111111 */
    torque_tmp |= ((unsigned long)byte_i << 0);
    byte_i = data[1];
    byte_i >>= 0;
    byte_i &= 0xff; /* Masking out bits 0b11111111 */
    torque_tmp |= ((unsigned long)byte_i << 8);
    handle->torque = torque_tmp * (1) + (0);
    
}

void SirenSprinklerStatus_encode(struct SirenSprinklerStatus_t* handle, uint8_t data[]) {
    data[0] = 0x00;
    data[1] = 0x00;
    data[2] = 0x00;
    data[3] = 0x00;
    data[4] = 0x00;
    data[5] = 0x00;
    data[6] = 0x00;
    data[7] = 0x00;
    // serializing Sprinkler4
    unsigned long Sprinkler4_tmp = (unsigned long)((handle->Sprinkler4 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler4_tmp << 3) & 0b1000);
    Sprinkler4_tmp >>= 1;
    // serializing Sprinkler2
    unsigned long Sprinkler2_tmp = (unsigned long)((handle->Sprinkler2 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler2_tmp << 1) & 0b10);
    Sprinkler2_tmp >>= 1;
    // serializing Sprinkler3
    unsigned long Sprinkler3_tmp = (unsigned long)((handle->Sprinkler3 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler3_tmp << 2) & 0b100);
    Sprinkler3_tmp >>= 1;
    // serializing Sprinkler1
    unsigned long Sprinkler1_tmp = (unsigned long)((handle->Sprinkler1 - (0)) / 1);
    data[0] = data[0] | ((Sprinkler1_tmp << 0) & 0b1);
    Sprinkler1_tmp >>= 1;
}

void SirenSprinklerStatus_decode(struct SirenSprinklerStatus_t* handle, uint8_t data[]) {
    uint8_t byte_i;
    // deserializing Sprinkler4
    unsigned long Sprinkler4_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 3;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler4_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler4 = Sprinkler4_tmp * (1) + (0);
    
    // deserializing Sprinkler2
    unsigned long Sprinkler2_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 1;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler2_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler2 = Sprinkler2_tmp * (1) + (0);
    
    // deserializing Sprinkler3
    unsigned long Sprinkler3_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 2;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler3_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler3 = Sprinkler3_tmp * (1) + (0);
    
    // deserializing Sprinkler1
    unsigned long Sprinkler1_tmp = 0x0;
    byte_i = data[0];
    byte_i >>= 0;
    byte_i &= 0x1; /* Masking out bits 0b1 */
    Sprinkler1_tmp |= ((unsigned long)byte_i << 0);
    handle->Sprinkler1 = Sprinkler1_tmp * (1) + (0);
    
}


void Siren_init(struct SirenDispatcher_t *handle){
    handle->user_data = NULL;
    handle->on_Sprinkle_Command_ptr = NULL;
    handle->on_Ping_ptr = NULL;
    handle->on_SprinklerStatus_ptr = NULL;
}

void Siren_dispatch(struct SirenDispatcher_t *handle, uint32_t arb_id, uint8_t data[]){
    struct SirenArbId arb_id_struct;
    SirenArbId_decode(&arb_id_struct, arb_id);
    if (
        (arb_id_struct.function_code==16)
    ){
        if (handle->on_Sprinkle_Command_ptr != NULL){
            struct SirenSprinkle_Command_t msg;
            SirenSprinkle_Command_decode(&msg, data);
            (*handle->on_Sprinkle_Command_ptr)(handle, arb_id, &msg);
        }
    }
    if (
        (arb_id_struct.function_code==255)&&(arb_id_struct.destination==255)
    ){
        if (handle->on_Ping_ptr != NULL){
            struct SirenPing_t msg;
            SirenPing_decode(&msg, data);
            (*handle->on_Ping_ptr)(handle, arb_id, &msg);
        }
    }
    if (
        (arb_id_struct.function_code==17)
    ){
        if (handle->on_SprinklerStatus_ptr != NULL){
            struct SirenSprinklerStatus_t msg;
            SirenSprinklerStatus_decode(&msg, data);
            (*handle->on_SprinklerStatus_ptr)(handle, arb_id, &msg);
        }
    }
}



/* initialize Sprinkle_Command message with message specific ID fields */
void SirenSprinkle_Command_init(struct SirenArbId* arb_id, struct SirenSprinkle_Command_t* data){
    arb_id->priority = 7;
    arb_id->function_code = 16;
    arb_id->data_page = 0;
    arb_id->reserved = 0;
    arb_id->destination = 0;
    arb_id->source_address = 0;
}

/* initialize Ping message with message specific ID fields */
void SirenPing_init(struct SirenArbId* arb_id, struct SirenPing_t* data){
    arb_id->priority = 7;
    arb_id->function_code = 255;
    arb_id->data_page = 0;
    arb_id->reserved = 0;
    arb_id->destination = 255;
    arb_id->source_address = 0;
}

/* initialize SprinklerStatus message with message specific ID fields */
void SirenSprinklerStatus_init(struct SirenArbId* arb_id, struct SirenSprinklerStatus_t* data){
    arb_id->priority = 7;
    arb_id->function_code = 17;
    arb_id->data_page = 0;
    arb_id->reserved = 0;
    arb_id->destination = 0;
    arb_id->source_address = 0;
}
