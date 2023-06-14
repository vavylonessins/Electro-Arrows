from types import LambdaType
from effects import *
from const import *
from levels import *
from gui import *
import gui


img_unknown = image.load("images/a_unknown.png")


class ChunkCacheTexture:
    def __init__(self, texture, tags):
        self.file = "cache/render/chunk_at_"+str(self.tags['x'])+"_"+str(self.tags['y'])+".png"
        self.__dict__.update(tags)
        self.texture = texture
        self.push()
    
    def push(self):
        gui.image.save(self.texture, self.file)
        del self.texture
    
    def pop(self):
        self.texture = gui.image.load(self.file)
    
    def get_texture(self):
        try:
            return self.texture
        except AttributeError or NameError:
            self.pop()
            texture = self.texture
            self.push()
            return texture
    
    def update(self, texture):
        self.texture = texture


class ChunkCacheTexturesContainer:
    def __init__(self):
        self.textures = []
    
    def append(self, texture: ChunkCacheTexture):
        self.textures.append(texture)
    
    def select(self, selector: LambdaType = lambda *a: True):
        ret = []
        for texture in self.textures:
            if selector(texture):
                ret.append(texture)
        return ret.copy()


class FlatChunkRenderer:
    def __init__(self, chunk: Chunk):
        self.chunk = chunk
        self.scale = 63
        self.renderers = {
            -1: self.r_unknown,
            0: self.r_empty
        }
    
    def set_scale(self, scale: int):
        self.scale = scale
        self.init_surface()
    
    def init_surface(self):
        self.surface = Surface((scale*8,scale*8))
    
    def render_all(self):
        self.init_surface()
        cell_surface = Surface((scale, scale))
        for x in range(8):
            for y in range(8):
                self.render_at(x, y, cell_surface)
        return ChunkCacheTexture(self.surface.copy(), {'x': self.chunk.x, 'y': self.chunk.y})
    
    def render_at(self, x, y, cell_surface):
        cell = self.chunk.get_at(x, y)
        cell_l = self.chunk.get_at(x-1, y)
        cell_t = self.chunk.get_at(x, y-1)
        cell_r = self.chunk.get_at(x+1, y)
        cell_b = self.chunk.get_at(x, y+1)
        cell_lt = self.chunk.get_at(x-1, y-1)
        cell_lb = self.chunk.get_at(x-1, y+1)
        cell_rt = self.chunk.get_at(x+1, y-1)
        cell_rb = self.chunk.get_at(x+1, y+1)
        cell_surface.fill(BACK)
        gui.draw.rect(cell_surface, MIDDLE, (0, 0, self.scale, self.scale), 1)
        try:
            self.renderers[cell](cell_surface, self.scale, cell_l, cell_b, cell_r, cell_t, cell_lt, cell_lb, cell_rt, cell_rb)
        except IndexError:
            self.renderers[-1](cell_surface, self.scale)
        self.surface.blit(cell_surface, (self.scale*x, self.scale*y))
    
    def r_empty(self, sc, scale, l, b, r, t, lt, lb, rt, rb):
        return

    def r_unknown(self, sc, scale, l, b, r, t, lt, lb, rt, rb):
        tex = gui.smoothscale(img_unknown, (scale, scale))
        sc.blit(tex, (0, 0))
        return


class DebugLevelRenderer:
    def __init__(self, level: Level, screen: Surface):
        self.screen = screen
        self.level = level
        self.screen_size = Vec2(self.sim_screen.get_size())
        self.scale = 63
        self.chunk_renderers: list[FlatChunkRenderer] = []
    
    def init(self):
        for c in self.level.chunks:
            self.chunk_renderers.append(FlatChunkRenderer(c))
    
    def set_scale(self, scale: int):
        self.scale = scale
        for cr in self.chunk_renderers:
            cr.set_scale(scale)
    
    def render_all(self, shift: Vec2 = Vec2(0, 0)):
        self.screen.fill(BACK)
        cache_textures: ChunkCacheTexturesContainer = ChunkCacheTexturesContainer()
        for cr in self.chunk_renderers:
            cache_textures.append(cr.render_all())
        for cct in cache_textures.textures:
            x = cct.x
            y = cct.y
            rel = Vec2(x*8*self.scale, y*8*self.scale)
            pos = rel-shift
            self.screen.blit(cct.get_texture(), pos)
