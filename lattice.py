import emath.tex as tex
import emath.eqn_cache as cache
import emath.math_render as mrend

import emath.make_eq as make_eq

import emath.question_manager as question_manager
from emath.latte_manager import LatteManager

import sympy

import pygame

pygame.init()
pygame.font.init()

WIDTH   = 1280
HEIGHT  = 720

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lattice β")

    context_manager = LatteManager(screen)

    clock = pygame.time.Clock()
    run = True
    while run:
        delta = clock.tick(240)
        screen.fill((0x20, 0x20, 0x20))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        context_manager.render()
        context_manager.update(events, delta)

        pygame.display.update()

    context_manager.close()


if __name__ == "__main__":
    main()
