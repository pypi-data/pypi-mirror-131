import pygame as pg
from dreammake.codekit import clamp, pad_rect
from pygame.color import THECOLORS as COLORS


# This class defines the Panel GUI element which acts as a sort of window and can contain other
# GUI elements.
class Panel:
    def __init__(self, position=(0, 0), caption="Panel", width=300, height=250, index=0):
        self.title_height = 20
        self.lbl_caption = Label(caption, fontcolor=COLORS["black"])
        self.lbl_caption.position = (10, self.title_height/2 - self.lbl_caption.height/2)

        # Size and position properties
        self.position = pg.Vector2(position)
        self._width = width
        self._height = height

        # Visual properties
        self.title_color = COLORS["gray"]
        self.fill_color = (255, 255, 255)
        self.alpha = 180
        self.title_rect = pg.Rect(self.position.x, self.position.y, self._width, self.title_height)
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)
        self.surface.convert_alpha()
        self.border_radius = 10
        self.border_size = 5

        # Event properties
        self.dragging = False
        self.drag_offset = pg.Vector2(0, 0)
        self.hiding = False
        self.focus = True
        self.locked = False
        self.grabbed = False
        self.index = 0

        self.resizable = True
        self.resize_handle_size = 8
        self.resize_handle = pg.Rect(self.get_rect().right - self.resize_handle_size, self.get_rect().bottom - self.resize_handle_size, self.resize_handle_size, self.resize_handle_size)
        self.dragging_resize = False
        self.min_size = (64, 64)
        self._isclicked = False

        # The organization of surfaces within the panel
        # Content to Content Surface
        # Content Surface to Panel Surface
        # Panel Surface to Display Surface
        # Content properties
        self.content_rect = pg.Rect(0, 0, self.width - 16, self.height - self.title_height - 16)
        self.base_surface = pg.Surface(self.content_rect.size)
        self.content_surface = pg.Surface(self.content_rect.size)
        self.content_offset = pg.Vector2(0, 0)

        self.elements = []
        self.scrollable = False

    # Create properties which ensure the correct updates take place when the user
    # attempts to resize the panel
    @property
    def width(self, width):
        self._width = width
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    @width.getter
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if width < self.min_size[0]:
            width = self.min_size[0]

        self._width = width
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    @property
    def height(self, height):
        self._height = height
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    @height.getter
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if height < self.min_size[1]:
            height = self.min_size[1]

        self._height = height
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    def get_rect(self):
        return pg.Rect(self.position.x, self.position.y, self.width, self.height)

    def hide(self):
        self.hiding = True

    def show(self):
        self.hiding = False

    def resize(self, xdiff, ydiff):
        self.width += xdiff
        self.height += ydiff
        self.base_surface = pg.Surface((self.width - 16, self.height - self.title_height - 16))
        #self.content_rect = pg.Rect(0, 0, self.width - 16, self.height - self.title_height - 16)
        self.content_surface = pg.Surface(self.content_rect.size)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.base_surface = pg.Surface((self.width - 16, self.height - self.title_height - 16))
        #self.content_rect = pg.Rect(0, 0, self.width - 16, self.height - self.title_height - 16)

        if self.content_rect.w < self.width:
            self.content_rect.w = self.width
        if self.content_rect.h < self.height:
            self.content_rect.h = self.height

        self.content_surface = pg.Surface(self.content_rect.size)

    def add_element(self, kind="label", *args):
        if kind == "label":
            new_label = Label(args[0], position=args[1])
            self.elements.append(new_label)

        elif kind == "button":
            new_button = Button(args[0], position=args[1])
            if len(args) >= 2:
                new_button.command = args[2]
            if len(args) > 3:
                new_button.args = args[3]
                print(args[3])
            self.elements.append(new_button)

        elif kind == "image":
            new_image = Image(args[0], args[1])
            self.elements.append(new_image)

        return self.elements[-1]

    def handle_element_events(self, events, mouse_pos):
        for element in self.elements:
            if type(element) == Button:
                element.handle_events(events, mouse_pos, self.position + (0, self.title_height))

    # Check if the user is interacting with the panel and respond appropriately
    def handle_events(self, events, mouse_pos):
        if not self.hiding:
            self.title_rect = pg.Rect(self.position.x, self.position.y, self._width, self.title_height)
            self.resize_handle = pg.Rect(self.get_rect().right - self.resize_handle_size,
                                         self.get_rect().bottom - self.resize_handle_size, self.resize_handle_size,
                                         self.resize_handle_size)

            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        if self.title_rect.collidepoint(mouse_pos):
                            self.drag_offset = mouse_pos - self.position
                            self.dragging = True

                        if self.resizable:
                            if self.resize_handle.collidepoint(mouse_pos):
                                self.dragging_resize = True

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == pg.BUTTON_LEFT:
                        self.dragging = False
                        self.dragging_resize = False

            if self.get_rect().collidepoint(mouse_pos):
                self.handle_element_events(events, mouse_pos)

    # Update the global rect objects on the panel to their correct position each frame
    def update(self, dt):
        if not self.hiding:
            mouse_pos = pg.mouse.get_pos()

            if self.dragging and not self.locked:
                self.position = pg.Vector2(mouse_pos) - self.drag_offset

            if self.resizable:
                if self.dragging_resize and not self.locked:
                    w = mouse_pos[0] - self.position.x
                    h = mouse_pos[1] - self.position.y
                    self.set_size(w, h)

            self.title_rect = pg.Rect(self.position.x, self.position.y, self._width, self.title_height)
            self.resize_handle = pg.Rect(self.get_rect().right-self.resize_handle.width,
                                         self.get_rect().bottom-self.resize_handle.height, self.resize_handle.width,
                                         self.resize_handle.height)

        if self.content_offset.x < -self.content_rect.w + self.base_surface.get_width():
            self.content_offset.x = -self.content_rect.w + self.base_surface.get_width()
        if self.content_offset.x > 0:
            self.content_offset.x = 0

        if self.content_offset.y < -self.content_rect.h + self.base_surface.get_height():
            self.content_offset.y = -self.content_rect.h + self.base_surface.get_height()
        if self.content_offset.y > 0:
            self.content_offset.y = 0

    def draw_elements(self, dest):
        for element in self.elements:
            element.draw(dest)

    def draw(self, dest):
        if not self.hiding:
            # Clear the panel surface
            self.surface.fill((0, 0, 0, 0))

            # Fill the body of the panel
            pg.draw.rect(self.surface, self.fill_color, (0, self.title_height-7, self.width, self._height-self.title_height+7), 0, self.border_radius)

            # Fill the title bar and patch the space between the rounded edges
            pg.draw.rect(self.surface, self.title_color, (0, 0, self._width, self.title_height), 0, self.border_radius)
            pg.draw.rect(self.surface, self.title_color, (0, self.title_height-self.border_radius, self._width, self.border_radius), 0)

            # Draw the border
            pg.draw.rect(self.surface, self.title_color, (0, 0, self._width, self._height), 1, self.border_radius)

            # Draw the caption label
            self.lbl_caption.draw(self.surface)

            # Clear the content surface
            self.base_surface.fill(COLORS["purple"])

            # Draw content to the content surface
            # for y in range(0, self.element_count):
            #     pg.draw.rect(self.content_surface, COLORS["white"], (self.content_offset.x, self.content_offset.y + y*100, 100, 100), 1)
            self.content_surface.fill(COLORS["white"])
            self.draw_elements(self.content_surface)
            self.base_surface.blit(self.content_surface, self.content_offset)

            # Blit the content surface to the panel
            self.surface.blit(self.base_surface, (1, self.title_height))

            # Finally blit the panel surface to the destination surface
            dest.blit(self.surface, self.position)
            pg.draw.rect(dest, COLORS["orange"], self.get_rect(), 1)


# This is the base class for any GUI element
class Element:
    def __init__(self, position, master=None):
        self.master = master
        self.position = pg.Vector2(position)


class Image(Element):
    def __init__(self, image, position):
        super().__init__(position)
        self.surface = image

    def draw(self, dest, offset=(0, 0)):
        dest.blit(self.surface, self.position)


# This defines the Label GUI element
class Label(Element):
    pg.font.init()

    def __init__(self, text="", size=16, fontcolor=(0, 0, 0), position=(0, 0), master=None):
        super().__init__(position, master)
        self._text = text
        self._fontsize = size
        self._fontcolor = fontcolor
        self._fontname = "arial"
        self._font = pg.font.SysFont(self._fontname, self._fontsize, False, False)
        self.surface = self._font.render(text, True, self._fontcolor)

    @property
    def width(self, width):
        pass

    @width.getter
    def width(self):
        return self.surface.get_width()

    @property
    def height(self, height):
        pass

    @height.getter
    def height(self):
        return self.surface.get_height()

    def get_size(self):
        return self.surface.get_size()

    def get_rect(self):
        return self.surface.get_rect()

    def update_surface(self):
        self.surface = self._font.render(self._text, True, self._fontcolor)

    def update_font(self):
        self._font = pg.font.SysFont(self._fontname, self._fontsize, False, False)

    @property
    def text(self, text):
        # If the text has not changed, do not update the surface
        if self._text != text:
            self._text = text
            self.update_surface()

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        # If the text has not changed, do not update the surface
        if self._text != text:
            self._text = text
            self.update_surface()

    @property
    def fontsize(self, size):
        if self._fontsize != size:
            self._fontsize = size
            self.update_font()
            self.update_surface()

    @fontsize.getter
    def fontsize(self):
        return self._fontsize

    @fontsize.setter
    def fontsize(self, size):
        if self._fontsize != size:
            self._fontsize = size
            self.update_font()
            self.update_surface()

    @property
    def fontcolor(self, color=(0, 0, 0)):
        # If the font color has not changed, do not update the surface
        if self._fontcolor != color:
            self._fontcolor = color
            self.update_surface()

    @fontcolor.getter
    def fontcolor(self):
        return self._fontcolor

    @fontcolor.setter
    def fontcolor(self, color=(0, 0, 0)):
        # If the font color has not changed, do not update the surface
        if self._fontcolor != color:
            self._fontcolor = color
            self.update_surface()

    def draw(self, dest):
        dest.blit(self.surface, self.position)


# This defines the Button GUI element
class Button(Element):
    def __init__(self, text="", position=(0, 0), command=None):
        super().__init__(position)
        self.label = Label(text, 15)

        # visual properties
        self.x_padding = 10
        self.y_padding = 4
        rect_width = self.label.width + self.x_padding*2
        rect_height = self.label.height + self.y_padding*2
        self.rect = pg.Rect(self.position[0], self.position[1], rect_width, rect_height)
        self.surface = pg.Surface((rect_width, rect_height), pg.SRCALPHA)
        self._width = rect_width
        self._height = rect_height
        self.label.position = pg.Vector2(self.width/2-self.label.width/2, self.height/2 - self.label.height/2)

        self.alpha = 200
        self.color = (169, 169, 169)
        self.bordercolor = (0, 0, 0, 255)
        self.bgcolor = self.color + (self.alpha,)
        self.hovercolor = self.color + (clamp(self.alpha + 200, 0, 255),)
        self.presscolor = self.color + (clamp(self.alpha + 250, 0, 255),)
        self.borderradius = 3

        # input handling properties
        self.hovering = False
        self.pressed = False
        self.command = command

        self.args = None

    @property
    def width(self, width):
        self._width = width
        self.rect = pg.Rect(self.position[0], self.position[1], self._width, self._height)
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    @width.getter
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self.rect = pg.Rect(self.position[0], self.position[1], self._width, self._height)
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)
        self.label.position = pg.Vector2(self.width/2-self.label.width/2, self.height/2 - self.label.height/2)

    @property
    def height(self, height):
        self._height = height
        self.rect = pg.Rect(self.position[0], self.position[1], self._width, self._height)
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)

    @height.getter
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self.rect = pg.Rect(self.position[0], self.position[1], self._width, self._height)
        self.surface = pg.Surface((self._width, self._height), pg.SRCALPHA)
        self.label.position = pg.Vector2(self.width/2-self.label.width/2, self.height/2 - self.label.height/2)

    def set_fontsize(self, size):
        self.label.fontsize = size
        rect_width = self.label.width + self.x_padding*2
        rect_height = self.label.height + self.y_padding*2
        self.rect = pg.Rect(self.position[0], self.position[1], rect_width, rect_height)
        self.width = self.rect.w
        self.height = self.rect.h

    def handle_events(self, events, mouse_pos, offset=(0, 0)):
        self.hovering = False

        self.rect.topleft = self.position
        if self.rect.collidepoint(pg.Vector2(mouse_pos) - pg.Vector2(offset)):
            self.hovering = True

        if self.hovering or self.pressed:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        self.pressed = True
                        if self.command:
                            if self.args is not None:
                                self.command(self.args)
                            else:
                                self.command()
                if self.pressed:
                    if event.type == pg.MOUSEBUTTONUP:
                        self.pressed = False

    def draw(self, dest):
        fillcolor = self.bgcolor
        if self.hovering:
            fillcolor = self.hovercolor
        if self.pressed:
            fillcolor = self.presscolor

        pg.draw.rect(self.surface, fillcolor, self.surface.get_rect(), 0, self.borderradius)
        pg.draw.rect(self.surface, self.bordercolor, self.surface.get_rect(), 1, self.borderradius)
        self.label.draw(self.surface)
        dest.blit(self.surface, self.position)


# The MenuBar is a menu in the form of a bar which can be used to call some method directly or open a drop menu.
class MenuBar(Element):
    def __init__(self, width, position=(0, 0)):
        super().__init__(position)
        self.height = 26
        self.width = width
        self.bar_color = (100, 100, 100, 200)
        self.bar_rect = pg.Rect(self.position.x, self.position.y, self.width, self.height)
        self.bar_surface = pg.Surface(self.bar_rect.size, pg.SRCALPHA)
        self.bar_surface.fill(self.bar_color)

        self._xoffset = 0
        self.buttons = {}

    def add_button(self, label, command=None):
        self.buttons[label] = Button(label, (self._xoffset, self.position.y))
        self.buttons[label].height = self.height
        self._xoffset += self.buttons[label].width

    def handle_events(self, events, mouse_pos):
        for button in self.buttons.values():
            button.handle_events(events, mouse_pos)

    def draw(self, dest):
        self.bar_surface.fill(self.bar_color)
        for button in self.buttons.values():
            button.draw(self.bar_surface)

        dest.blit(self.bar_surface, (0, 0))


# A DropMenu is simply a drop down menu with some commands in the form of buttons
# ( Implement cascades )
class DropMenu(Element):
    dropmenu_collection = []

    def __init__(self, position=(0, 0), master=None):
        super().__init__(position, master)
        self.buttons = {}
        self.button_height = 26
        self._yoffset = 0
        self._maxwidth = 0
        self.hidden = True
        self.padding = 3
        self.border_rect = pg.Rect(self.position.x, self.position.y, 0, 0)
        self.bg_surface = pg.Surface(self.border_rect.size, pg.SRCALPHA)
        self.bg_color = COLORS["white"]
        DropMenu.dropmenu_collection.append(self)

    def add_button(self, label, command=None):
        self.buttons[label] = Button(label, (self.position.x, self.position.y + self._yoffset), command)
        self.buttons[label].height = self.button_height
        self._yoffset += self.button_height

        if self.buttons[label].width > self._maxwidth:
            self._maxwidth = self.buttons[label].width

        self.border_rect.width = self._maxwidth
        self.border_rect.height = self._yoffset
        self.border_rect = pad_rect(self.border_rect, self.padding, self.padding)
        self.bg_surface = pg.Surface(self.border_rect.size, pg.SRCALPHA)
        self.bg_surface.fill(self.bg_color)
        for button in self.buttons.values():
            button.width = self._maxwidth

    def show(self):
        # Make sure all other drop menus are hidden
        for dropmenu in DropMenu.dropmenu_collection:
            dropmenu.hide()

        self.hidden = False

    def hide(self):
        self.hidden = True

    def handle_events(self, events, mouse_pos):
        # Create an copy of the border rect, move it up and increase the height to make a buffer area in which the
        # mouse will be registered as colliding with the active area of the drop menu.
        extended_rect = self.border_rect.copy()
        extended_rect.y -= self.button_height + 6
        extended_rect.h += self.button_height + 6

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    for button in self.buttons.values():
                        if button.pressed:
                            self.hide()

        if not self.hidden:
            for button in self.buttons.values():
                button.handle_events(events, mouse_pos)
                if button.pressed:
                    self.hide()
                    button.pressed = False
                    
            if not extended_rect.collidepoint(mouse_pos):
                self.hide()

    def draw(self, dest):
        if not self.hidden:
            self.bg_surface.fill(self.bg_color)
            dest.blit(self.bg_surface, self.position - (self.padding, self.padding))

            for button in self.buttons.values():
                button.draw(dest)


class VerticalScrollbar(Element):
    def __init__(self, position, width, height):
        super().__init__(position)
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.surface = pg.Surface(self.rect.size)

        self.arrow_size = self.rect.w
        self.up_button = Button(" ", self.position)
        self.up_button.width = self.arrow_size
        self.up_button.height = self.arrow_size

        self.down_button = Button(" ", self.rect.bottomleft - pg.Vector2(0, self.arrow_size))
        self.down_button.width = self.arrow_size
        self.down_button.height = self.arrow_size

        self.slider_button = Button("||", (self.position[0], self.position[1]))
        self.slider_button.borderradius = 0
        self.slider_button.position.y = self.position.y + self.arrow_size
        self.slider_button.width = self.rect.width

        self.content_height = 400
        self.sliding = False
        self.dragoffset = 0
        self.button_offset = self.arrow_size

    def handle_events(self, events, mouse_pos, offset=(0, 0)):
        self.slider_button.handle_events(events, mouse_pos, offset)
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    self.sliding = False

        if self.slider_button.pressed:
            self.sliding = True
            self.dragoffset = mouse_pos[1] - self.slider_button.position.y
            self.slider_button.pressed = False

        self.up_button.handle_events(events, mouse_pos)
        self.down_button.handle_events(events, mouse_pos)

    def update(self, dt):
        self.up_button.position = self.rect.topleft
        self.down_button.position = pg.Vector2(self.rect.bottomleft) - pg.Vector2(0, self.arrow_size)

        if self.sliding:
            self.slider_button.position.y = pg.mouse.get_pos()[1] - self.dragoffset

        # Limit the slider button from going outside the rail
        if self.slider_button.position.y < self.rect.y + self.arrow_size:
            self.slider_button.position.y = self.rect.y + self.arrow_size
        elif self.slider_button.position.y > self.rect.bottom - self.arrow_size - self.slider_button.height + 1:
            self.slider_button.position.y = self.rect.bottom - self.arrow_size - self.slider_button.height + 1

        # Change the height of the slider button in relation to the height of the content rect and the height of the
        # view height
        rail_height = self.rect.h - (self.arrow_size*2)

        self.slider_button.height = (rail_height/self.content_height) * rail_height

        if self.slider_button.height > rail_height:
            self.slider_button.height = rail_height

        self.slider_button.position.x = self.rect.x

    def draw(self, dest, offset=(0, 0)):
        # Draw the background
        pg.draw.rect(dest, (20, 100, 100), self.rect)

        # Draw the outline
        pg.draw.rect(dest, (255, 255, 255), self.rect, 1)

        # Draw up button
        self.up_button.draw(dest)

        # Draw down button
        self.down_button.draw(dest)

        # Draw the slider button
        #pg.draw.rect(dest, (0, 0, 0), (self.rect.left, self.rect.top + sbw, self.rect.w, 100))
        self.slider_button.draw(dest)


class Dragbox(Element):
    def __init__(self, position, size):
        super().__init__(position)
        self.rect = pg.Rect(0, 0, size, size)
        self.rect.center = position
        self.dragging = False
        self.snap_size = 8

    def handle_events(self, events, mouse_pos):
        self.rect.center = self.position
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    if self.rect.collidepoint(mouse_pos):
                        self.dragging = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    self.dragging = False

        if self.dragging:
            self.position = mouse_pos

    def update(self, dt):
        pass

    def draw(self, dest, offset=(0, 0), color=COLORS["red"]):
        offset_rect = pg.Rect(self.rect.x + offset[0], self.rect.y + offset[1], self.rect.w, self.rect.h)
        pg.draw.rect(dest, color, offset_rect, 1)


class ImageButton(Element):
    def __init__(self, position, image):
        super().__init__(position)
        self.image = image

    def draw(self, dest, offset=(0, 0)):
        dest.blit(self.image, self.position + offset)


# This class will handle the creation, event handling, updating and rendering of all GUI elements
# within a single application or scene
class UIManager:
    def __init__(self, screen_rect):
        self.panels = []
        self.boundary_rect = pg.Rect(screen_rect)
        self.focus_indices = [x for x in range(len(self.panels))]
        self.menubar = MenuBar(self.boundary_rect.width)

    def add_panel(self, position, size, caption="Panel"):
        new_panel = Panel(position, caption, size[0], size[1])
        new_panel.index = len(self.focus_indices)
        self.panels.append(new_panel)
        self.focus_indices = [x for x in range(len(self.panels))]
        return new_panel

    def set_focus_panel(self, panel):
        # If the given panel is not already the focus panel, swap the panel with the last item in the focus order
        self.focus_indices.sort(key=panel.index.__eq__)

    def handle_events(self, events, mouse_pos):
        # Loop through the panels in order of focus and check if the mouse is within its rect. If so, we return
        # effectively preventing any mouse clicks from interacting with panels beneath other panels.
        # In summary, you cannot click any elements or panels being covered by other panels.
        # We will need to implement a similar system for menubars and other loose elements (Not within a panel)
        for i in reversed(self.focus_indices):
            self.panels[i].handle_events(events, mouse_pos)
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        if self.panels[i].get_rect().collidepoint(mouse_pos) or \
                                self.panels[i].resize_handle.collidepoint(mouse_pos):
                            self.set_focus_panel(self.panels[i])
                            return
            if self.panels[i].get_rect().collidepoint(mouse_pos):
                return

            self.menubar.handle_events(events, mouse_pos)

    def update(self, dt):
        for i in self.focus_indices:
            self.panels[i].update(dt)
            if self.panels[i].position.x < self.boundary_rect.left:
                self.panels[i].position.x = self.boundary_rect.left
            if self.panels[i].position.y < self.boundary_rect.top:
                self.panels[i].position.y = self.boundary_rect.top

            if self.panels[i].position.x + self.panels[i].width > self.boundary_rect.right:
                self.panels[i].position.x = self.boundary_rect.right - self.panels[i].width
            if self.panels[i].position.y + self.panels[i].height > self.boundary_rect.bottom:
                self.panels[i].position.y = self.boundary_rect.bottom - self.panels[i].height

            if self.panels[i].dragging or self.panels[i].dragging_resize:
                self.set_focus_panel(self.panels[i])
            if self.panels[i]._isclicked is True:
                self.set_focus_panel(self.panels[i])
                self.panels[i]._isclicked = False

    def draw(self, dest):

        # Draw our UI Panels in order of most recently focused
        for i in self.focus_indices:
            self.panels[i].draw(dest)

        # DEBUG ( Render panel rects on focus )
        # for i in reversed(self.focus_indices):
        #     if self.panels[i].get_rect().collidepoint(pg.mouse.get_pos()) or \
        #         self.panels[i].resize_handle.collidepoint(pg.mouse.get_pos()):
        #         pg.draw.rect(dest, COLORS["green"], self.panels[i].get_rect(), 1)
        self.menubar.draw(dest)

