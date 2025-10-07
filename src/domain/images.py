import pygame

# ~~~~~~~~~~===> Items's images <===~~~~~~~~~~
piece_anim = [
    pygame.image.load('src/assets/items/piece/anim_1.png').convert_alpha(),
    pygame.image.load('src/assets/items/piece/anim_2.png').convert_alpha(),
    pygame.image.load('src/assets/items/piece/anim_3.png').convert_alpha(),
    pygame.image.load('src/assets/items/piece/anim_4.png').convert_alpha()
]

# ~~~~~~~~~~===> Caracter's images <===~~~~~~~~~~

caracter_bottom_walks = [
    pygame.image.load('src/assets/caracters/caracter/walking/bottom/anim_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/bottom/anim_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/bottom/anim_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/bottom/anim_4.png').convert_alpha()
]

caracter_left_walks = [
    pygame.image.load('src/assets/caracters/caracter/walking/left/anim_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/left/anim_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/left/anim_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/left/anim_4.png').convert_alpha()
]

caracter_top_walks = [
    pygame.image.load('src/assets/caracters/caracter/walking/top/anim_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/top/anim_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/top/anim_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/top/anim_4.png').convert_alpha()
]

caracter_right_walks = [
    pygame.image.load('src/assets/caracters/caracter/walking/right/anim_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/right/anim_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/right/anim_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caracter/walking/right/anim_4.png').convert_alpha()
]

# ~~~~~~~~~~===> Sarah's images <===~~~~~~~~~~

sarah_bottom_walks =  [
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/bottom/sprite_9.png').convert_alpha(),
    ]

sarah_left_walks =  [
    pygame.image.load('src/assets/caracters/sarah/left/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/left/sprite_9.png').convert_alpha(),
    ]

sarah_top_walks =  [
    pygame.image.load('src/assets/caracters/sarah/top/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/top/sprite_9.png').convert_alpha(),
    ]

sarah_right_walks =  [
    pygame.image.load('src/assets/caracters/sarah/right/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/sarah/right/sprite_9.png').convert_alpha(),
    ]

# ~~~~~~~~~~===> Emma's images <===~~~~~~~~~~
emma_bottom_walks =  [
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/bottom/sprite_9.png').convert_alpha(),
    ]

emma_left_walks =  [
    pygame.image.load('src/assets/caracters/emma/left/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/left/sprite_9.png').convert_alpha(),
    ]

emma_top_walks =  [
    pygame.image.load('src/assets/caracters/emma/top/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/top/sprite_9.png').convert_alpha(),
    ]

emma_right_walks =  [
    pygame.image.load('src/assets/caracters/emma/right/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/emma/right/sprite_9.png').convert_alpha(),
    ]

# ~~~~~~~~~~===> Caporal's images <===~~~~~~~~~~
caporal_bottom_walks =  [
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/bottom/sprite_9.png').convert_alpha(),
    ]

caporal_left_walks =  [
    pygame.image.load('src/assets/caracters/caporal/left/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/left/sprite_9.png').convert_alpha(),
    ]

caporal_top_walks =  [
    pygame.image.load('src/assets/caracters/caporal/top/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/top/sprite_9.png').convert_alpha(),
    ]

caporal_right_walks =  [
    pygame.image.load('src/assets/caracters/caporal/right/sprite_1.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_2.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_3.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_4.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_5.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_6.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_7.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_8.png').convert_alpha(),
    pygame.image.load('src/assets/caracters/caporal/right/sprite_9.png').convert_alpha(),
    ]

#Etienne <3