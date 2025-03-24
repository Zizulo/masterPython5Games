# draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            # load health bar
            self.load_life(self.lifes)

            pygame.display.update()
