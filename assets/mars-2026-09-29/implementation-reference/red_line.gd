extends Node2D

const ENDING = ["MAX\n\ndlg.red_line.max.005", "ANDYGEN\n\ndlg.red_line.andygen.006", "MAX\n\ndlg.red_line.max.007"]
const DEBRIEF = "Transport belt crossed. Mars Industrial runs at 310% output despite the Earth lockdown. The factories still accept orders from an unknown source."
const TRANSMISSIONS = [
    {"at":0.0,"speaker":"MAX","text":"dlg.red_line.max.001"},
    {"at":5.0,"speaker":"ANDYGEN","text":"dlg.red_line.andygen.008"},
    {"at":8.0,"speaker":"MAX","text":"dlg.red_line.max.002"},
]
const TIMES = [16.0, 30.0, 44.0, 58.0, 72.0, 86.0, 100.0, 114.0]
var game: Node2D
var next_machine := 0
var cleared := false
var collisions := 0
var machinery_hull_damage := 0
var passed := 0
var machinery: Array[Node2D] = []

static func build() -> Array[Dictionary]:
    var waves: Array[Dictionary] = []
    var formation = preload("res://scripts/missions/mercury_1_1_timeline.gd")
    for i in range(9):
        var kind: String = ["scout","scout","striker","guard","scout","striker","guard","striker","guard"][i]
        waves.append({"at":13.0+i*12.0,"name":"MARS / "+kind.to_upper(),"spawns":formation._line(kind,2 if kind == "guard" else 3,180,160,0.85)})
    return waves

func _ready() -> void:
    game = get_parent()

func _process(_delta: float) -> void:
    if game.game_over or cleared:
        return
    if next_machine < TIMES.size() and game.elapsed >= TIMES[next_machine]:
        deploy(next_machine)
        next_machine += 1
    machinery = machinery.filter(func(machine): return is_instance_valid(machine) and not machine.is_queued_for_deletion())
    cleared = next_machine == TIMES.size() and passed == TIMES.size() and machinery.is_empty() and game.elapsed >= 126.0

func deploy(index: int) -> Node2D:
    var machine = preload("res://scripts/hazards/industrial_machinery.gd").new()
    machine.controller = self
    machine.kind = "loader" if index%2 == 0 else "arm"
    machine.from_right = index%4 in [1,2]
    machine.lane_y = game.viewport_size.y * [0.64,0.59,0.73,0.64,0.54,0.69,0.68,0.57][index%8]
    add_child(machine)
    machinery.append(machine)
    if machine.kind == "loader":
        game.hud.show_transmission("ROOK","dlg.red_line.rook.003",3,3.0)
    else:
        game.hud.show_transmission("ROOK",tr("dlg.red_line.rook.004") % ("Right" if machine.from_right else "Left"),3,3.0)
    return machine

func register_contact() -> void:
    # Physical contact is a separate star condition, even if shields or immunity absorb damage.
    collisions += 1
    var before: int = game.player.get_health()
    game.player.take_damage(1)
    machinery_hull_damage += maxi(0,before-game.player.get_health())
