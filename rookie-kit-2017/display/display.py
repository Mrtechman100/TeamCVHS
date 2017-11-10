#
# This file is where you make the display for your game
# Make changes and add functions as you need.
#

import pygame
from config import *
from tps.common.event import *
from tps.client.base_display import BaseDisplay
import os


class Display(BaseDisplay):
    """
    This class controls all of the drawing of the screen
    for your game.  The process of drawing a screen is
    to first draw the background, and then draw everything
    that goes on top of it.  If two items are drawn in the
    same place, then the last item drawn will be the one
    that is visible.

    The screen is a 2 dimensional grid of pixels, with the
    origin (0,0) located at the top-left of the screen, and
    x values increase to the right and y values increase as
    you go down.  The y values are opposite of what you learned
    in your math classes.

    Documentation on drawing in pygame is available here:
    http://www.pygame.org/docs/ref/draw.html

    The methods in this class are:
    __init__ creates data members (variables) that are used
        in the rest of the methods of this class.  This is
        useful for defining colors and sizes, loading image
        or sound files, creating fonts, etc.  Basically,
        any one time setup.

    paint_game controls the drawing of the screen while the
        game is in session.  This is responsible for making
        sure that any information, whether graphics, text, or
        images are drawn to the screen.

    paint_waiting_for_game controls the drawing of the screen
        after you have requested to join a game, but before
        the game actually begins.
    
    paint_game_over controls the drawing of the screen after
        the game has been won, but before the game goes away.
        This is a short (3-5 second) period.

    process_event controls handling events that occur in the
        game, that aren't represented by objects in the game
        engine.  This includes things like collisions,
        objects dying, etc.  This would be a great place to
        play an audio file when missiles hit objects.

    paint_pregame controls the drawing of the screen before
        you have requested to join a game.  This would usually
        allow the user to know the options available for joining
        games.

    Method parameters and data members of interest in these methods:
    self.width is the width of the screen in pixels.
    self.height is the height of the screen in pixels.
    self.* many data members are created in __init__ to set up
        values for drawing, such as colors, text size, etc.
    surface is the screen surface to draw to.
    control is the control object that is used to
        control the game using user input.  It may
        have data in it that influences the display.
    engine contains all of the game information about the current
        game.  This includes all of the information about all of
        the objects in the game.  This is where you find all
        of the information to display.
    event is used in process_event to communicate what
        interesting thing occurred.
    
    Note on text display:  There are 3 methods to assist
    in the display of text.  They are inherited from the
    BaseDisplay class.  See client/base_display.py.
    
    """

    def __init__(self, width, height):
        """
        Configure display-wide settings and one-time
        setup work here.
        """
        pygame.mixer.init()
        pygame.mixer.music.load('sounds\Lit.ogg')
        pygame.mixer.music.play(-1)
        self.hugesound = pygame.mixer.Sound('sounds\Fire.wav')
        self.firesound = pygame.mixer.Sound('sounds\Huge.wav')
        BaseDisplay.__init__(self, width, height)

        file_path = os.path.join('img', 'Title.png')
        self.titleimg = pygame.image.load(file_path)

        file_path = os.path.join('img', 'wall.png')
        self.wall = pygame.image.load(file_path)

        file_path = os.path.join('img', 'loading.png')
        self.loading = pygame.image.load(file_path)

        file_path = os.path.join('img', 'dollar.png')
        self.dollar = pygame.image.load(file_path)

        file_path = os.path.join('img', 'kim.png')
        self.kim = pygame.image.load(file_path)

        file_path = os.path.join('img', 'background.png')
        self.background = pygame.image.load(file_path)

        file_path = os.path.join('img', 'trump.png')
        self.trump = pygame.image.load(file_path)

        file_path = os.path.join('img', 'bottle.png')
        self.bottle = pygame.image.load(file_path)

        file_path = os.path.join('img', 'egl.png')
        self.egl = pygame.image.load(file_path)
        
        # There are other fonts available, but they are not
        # the same on every computer.  You can read more about
        # fonts at http://www.pygame.org/docs/ref/font.html
        self.font_size = 12
        self.font = pygame.font.SysFont("Courier New",self.font_size)

        # Colors are specified as a triple of integers from 0 to 255.
        # The values are how much red, green, and blue to use in the color.
        # Check out http://www.colorpicker.com/ if you want to try out
        # colors and find their RGB values.   Be sure to use the `R`, `G`,
        # `B` values at the bottom, not the H, S, B values at the top.
        self.player_color     = (0, 255, 0)
        self.opponent_color   = (255, 0, 0)
        self.missile_color    = (0, 255, 255)
        self.npc_color        = (255, 255, 0)
        self.wall_color       = (255, 255, 255)
        self.text_color       = (255, 255, 255)
        self.background_color = (0, 0, 0)
        return

    def paint_pregame(self, surface, control):
        """
        Draws the display before the user selects the game type.
        """
        # background
        file_path = os.path.join('img', 'Title.png')
        image = pygame.image.load(file_path)
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        surface.blit(self.titleimg, rect)
        # text message in center of screen
        
        return
        
    def paint_waiting_for_game(self, surface, engine, control):
        """
        Draws the display after user selects the game type, before the game begins.
        This is usually a brief period of time, while waiting for an opponent
        to join the game.
        """
        # background
        file_path = os.path.join('img', 'loading.png')
        image = pygame.image.load(file_path)
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        surface.blit(self.loading, rect)
        
        return

    def paint_game(self, surface, engine, control):
        """
        Draws the display after the game starts.
        """
        # background
        file_path = os.path.join('img', 'background.png')
        image = pygame.image.load(file_path)
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        surface.blit(self.background, rect)
            
        # draw each object
        objs = engine.get_objects()
        for key in objs:
            obj = objs[key]
            if obj.is_wall():
                self.paint_wall(surface, engine, control, obj)
            elif obj.is_npc():
                self.paint_npc(surface, engine, control, obj)
            elif obj.is_missile():
                self.paint_missile(surface, engine, control, obj)
            elif obj.is_player():
                self.paint_player(surface, engine, control, obj)
            else:
                print("Unexpected object type: %s" % (str(obj.__class__)))
                
        # draw game data
        if control.show_info:
            self.paint_game_status(surface, engine, control)
        return

        
    def paint_game_over(self, surface, engine, control):
        """
        Draws the display after the game ends.  This
        chooses to display the game, and add a game over
        message.
        """
        self.paint_game(surface, engine, control)
        
        s = "Game Over (%s wins!)" % (engine.get_winner_name())
        self.draw_text_center(surface, s, self.text_color, int(self.width/2), int(self.height/2), self.font)
        return

    def process_event(self, surface, engine, control, event):
        """
        Should process the event and decide if it needs to be displayed, or heard.
        """
        if event.get_kind()==E_MISSILE_FIRE:
            self.hugesound.play()
        if event.get_kind()==E_MISSILE_HIT:
            self.firesound.play()
        return

    # The following methods draw appropriate rectangles
    # for each of the objects, by type.
    # Most objects have an optional text display to
    # demonstrate how to send information from the control
    # to the display.
    def paint_wall(self, surface, engine, control, obj):
        """
        Draws walls.
        """
        rect = self.obj_to_rect(obj)
        file_path = os.path.join('img', 'wall.png')
        image = pygame.image.load(file_path)
        rect = self.obj_to_rect(obj)
        surface.blit(self.wall, rect)
        return
        
    def paint_npc(self, surface, engine, control, obj):
        """
        Draws living NPCs.
        """
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            file_path = os.path.join('img', 'dollar.png')
            image = pygame.image.load(file_path)
            rect = self.obj_to_rect(obj)
            surface.blit(self.dollar, rect)
        return
        
    def paint_missile(self, surface, engine, control, obj):
        """
        Draws living missiles.
        """
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            if obj.get_player_oid() == engine.get_player_oid():
                color = self.player_color
                file_path = os.path.join('img', 'egl.png')
                image = pygame.image.load(file_path)
                rect = self.obj_to_rect(obj)
                surface.blit(self.egl, rect)
            else:
                color = self.opponent_color
                file_path = os.path.join('img', 'bottle.png')
                image = pygame.image.load(file_path)
                rect = self.obj_to_rect(obj)
                surface.blit(self.bottle, rect)
        return
        
    def paint_player(self, surface, engine, control, obj):
        """
        Draws living players.
        My player is my opponent are in different colors
        """
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            if obj.get_oid() == engine.get_player_oid():
                color = self.player_color
                file_path = os.path.join('img', 'trump.png')
                image = pygame.image.load(file_path)
                rect = self.obj_to_rect(obj)
                surface.blit(self.trump, rect)
            else:
                color = self.opponent_color
                file_path = os.path.join('img', 'kim.png')
                image = pygame.image.load(file_path)
                rect = self.obj_to_rect(obj)
                surface.blit(self.kim, rect)
        return

    def paint_game_status(self, surface, engine, control):
        """
        This method displays some text in the bottom strip
        of the screen.  You can make it do whatever you want,
        or nothing if you want.
        """

        # display my stats
        oid = engine.get_player_oid()
        if oid > 0: 
            obj = engine.get_object(oid)
            if obj:
                s = ("Me: %s  HP: %.1f  XP: %.1f Mv: %.1f Ms: %.1f" % \
                    (engine.get_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana()))
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 3 * self.font_size / 2
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)
                
        # display opponent's stats
        oid = engine.get_opponent_oid()
        if oid > 0: 
            obj = engine.get_object(oid)
            if obj:
                s = "Opponent: %s  HP: %.1f  XP: %.1f Mv: %.1f Ms: %.1f" % \
                    (engine.get_opponent_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana())
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 6 * self.font_size / 2
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)
        return

