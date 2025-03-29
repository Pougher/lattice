import emath.tex as tex
import emath.eqn_cache as cache
import emath.math_render as mrend

import emath.make_eq as make_eq

import sympy

import pygame

pygame.init()

x = sympy.Symbol('x')
e = sympy.Symbol('e')
exp = make_eq.EquationBuilder().make_random_equation(4)
c = cache.EquationCache()
c.unload_all()
c.save_equation_cache()

WIDTH   = 1280
HEIGHT  = 720

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lattice β")

    math_renderer = mrend.MathRenderer(WIDTH, HEIGHT)
    math_renderer.add_scaled(r"$" + sympy.latex(sympy.diff(exp, x)) + "$", [0, 0])

    run = True
    while run:
        screen.fill((0xe0, 0xb0, 0x2f))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

        math_renderer.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
