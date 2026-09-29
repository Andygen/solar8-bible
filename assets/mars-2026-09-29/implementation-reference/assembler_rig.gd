extends Node2D

# Port of the user-provided assembler-rig.js. Pivots stay in original PNG pixels.
const ORIGIN := Vector2(550,535)
const SOCKETS = [Vector2(207,188),Vector2(1047,188),Vector2(207,925),Vector2(1047,925)]
var textures: Dictionary = {}
var sprites: Dictionary = {}
var wrists: Array[Vector2] = []
var disabled_at := [-1.0,-1.0,-1.0,-1.0]
var opening := 0.0
var age := 0.0

func _ready() -> void:
    for part in ["chassis","base","upper","forearm","jaw","drill","saw","hatch","press","core"]:
        textures[part] = load("res://assets/art/mars/assembler/assembler-"+part+".png")
    pose(0,0)

func _place(key: String, part: String, point: Vector2, angle: float, factor: float, pivot: Vector2, mirror := 1.0) -> Sprite2D:
    if not sprites.has(key):
        var sprite := Sprite2D.new()
        sprite.texture = textures[part]
        sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
        add_child(sprite)
        sprites[key] = sprite
    var node: Sprite2D = sprites[key]
    var source_size := Vector2(887,1774) if part == "hatch" else Vector2(1254,1254)
    var ratio: Vector2 = source_size/node.texture.get_size()
    node.offset = (source_size*0.5-pivot)/ratio
    node.scale = ratio*factor*Vector2(mirror,1)
    node.rotation = angle
    node.position = point-ORIGIN
    return node

func pose(seconds: float, slide: float) -> void:
    age = seconds
    opening = slide
    wrists.clear()
    _place("chassis","chassis",ORIGIN,0,0.5,Vector2(627,627))
    var core := _place("core","core",Vector2(550,490),0,0.2,Vector2(627,627))
    core.visible = opening > 35
    _place("hatch_l","hatch",Vector2(506-slide,490),0,0.14,Vector2(444,887))
    _place("hatch_r","hatch",Vector2(594+slide,490),0,0.14,Vector2(444,887),-1)
    var reveal := clampf((opening-35)/63,0,1)
    var t := seconds/10.0
    _place("press","press",Vector2(550,411-87*reveal+12*sin(t*TAU)*(1-reveal)),0,0.14,Vector2(627,627))
    for i in range(4):
        var cycle: float = t if disabled_at[i] < 0 else disabled_at[i]/10.0
        var side := -1.0 if i%2 == 0 else 1.0
        var bottom := i > 1
        var w := sin(cycle*TAU+i*0.6)
        var shoulder: Vector2 = ORIGIN+(SOCKETS[i]-Vector2(627,627))*0.5
        var base_angle: float = (150 if side < 0 else 30) if bottom else (-150 if side < 0 else -30)
        var a := deg_to_rad(base_angle+side*8*w)
        var b := deg_to_rad(((-60 if side < 0 else 60) if bottom else (-90 if side < 0 else 90))+side*12*w)
        var elbow := shoulder+Vector2.from_angle(a)*125
        var wrist := elbow+Vector2.from_angle(a+b)*105
        wrists.append(wrist-ORIGIN)
        var prefix := "arm"+str(i)
        _place(prefix+"base","base",shoulder,0,0.085,Vector2(627,604))
        _place(prefix+"upper","upper",shoulder,a,125.0/829,Vector2(210,620))
        _place(prefix+"cap1","base",shoulder,0,0.015,Vector2(627,604))
        _place(prefix+"forearm","forearm",elbow,a+b-atan2(4,843),105.0/Vector2(843,4).length(),Vector2(235,620))
        _place(prefix+"cap2","base",elbow,0,0.019,Vector2(627,604))
        var direction := a+b+PI/2
        if i == 1:
            _place(prefix+"tool","drill",wrist,direction,0.105,Vector2(627,967))
        elif i == 2:
            _place(prefix+"tool","saw",wrist,cycle*PI*8,0.105,Vector2(627,612))
            _place(prefix+"cap3","base",wrist,0,0.021,Vector2(627,604))
        else:
            _place(prefix+"tool","base",wrist,direction,0.059,Vector2(627,604))
            var spread := deg_to_rad(8+14*(0.5+0.5*sin(cycle*TAU+i)))
            _place(prefix+"jaw_l","jaw",wrist+Vector2(-20,-5).rotated(direction),direction-spread,0.074,Vector2(599,951))
            _place(prefix+"jaw_r","jaw",wrist+Vector2(20,-5).rotated(direction),direction+spread,0.074,Vector2(599,951),-1)
        for key in sprites:
            if key.begins_with(prefix):
                sprites[key].modulate = Color(0.32,0.32,0.32) if disabled_at[i] >= 0 else Color.WHITE

func disable_arm(index: int) -> void:
    disabled_at[index] = age
