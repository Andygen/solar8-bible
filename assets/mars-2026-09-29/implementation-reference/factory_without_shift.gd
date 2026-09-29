extends Node2D

const Target = preload("res://scripts/missions/factory_target.gd")
const ENDING = ["MAX\n\ndlg.mars_4_2.ending.max.001", "LENA\n\ndlg.mars_4_2.ending.lena.002", "MAX\n\ndlg.mars_4_2.ending.max.003"]
const DEBRIEF = "Assembly cradles disabled. Max found components outside the human design catalog. The production network leads deeper into Mars Industrial."
var game: Node2D
var units: Array[Area2D] = []
var cradles_destroyed := 0
var repairs_completed := 0
var production_count := 0
var next_repair := 0
var cleared := false
var warned := false
var assembly_story := false
var pending_dialogue: Array[Dictionary] = []
var dialogue_clock := 0.0

func _ready() -> void:
    game = get_parent()
    for i in range(3):
        make_unit("cradle", Vector2(game.viewport_size.x * [0.22,0.5,0.78][i], game.viewport_size.y * 0.27))
    make_unit("guard", Vector2(game.viewport_size.x * 0.35, game.viewport_size.y * 0.44))
    make_unit("guard", Vector2(game.viewport_size.x * 0.65, game.viewport_size.y * 0.44))

func make_unit(kind: String, point: Vector2) -> Area2D:
    var unit := Target.new()
    unit.controller = self
    unit.kind = kind
    unit.position = point
    add_child(unit)
    units.append(unit)
    game.total_targets += 1
    return unit

func _process(delta: float) -> void:
    if game.game_over or cleared:
        return
    units = units.filter(func(unit): return is_instance_valid(unit) and not unit.is_queued_for_deletion())
    if next_repair < 2 and game.elapsed >= [12.0,42.0][next_repair] and cradles_destroyed < 3:
        make_unit("repair",Vector2(game.viewport_size.x * (0.76 if next_repair == 0 else 0.24), game.viewport_size.y * 0.39))
        next_repair += 1
    dialogue_clock -= delta
    if dialogue_clock <= 0 and not pending_dialogue.is_empty():
        var line: Dictionary = pending_dialogue.pop_front()
        game.hud.show_transmission(line.speaker, line.text, 2, 4.0)
        dialogue_clock = 4.5
    var living := units.filter(func(unit): return not unit.wreck and not unit.finished)
    cleared = cradles_destroyed == 3 and living.is_empty() and game.get_tree().get_nodes_in_group("enemies").is_empty()
    game.wave_label.text = tr("FACTORY %d/3") % cradles_destroyed

func active_defenders() -> int:
    return game.get_tree().get_nodes_in_group("enemies").size() - (3-cradles_destroyed)

func produce(cradle: Area2D, cycle: int) -> void:
    production_count += 1
    if cycle % 3 == 2:
        make_unit("guard", Vector2(cradle.position.x, game.viewport_size.y * 0.45))
    else:
        game.total_targets += 1
        var enemy: Node2D = game._spawn_enemy_job({"kind":"scout" if cycle % 2 == 0 else "striker", "x":cradle.position.x, "y":cradle.position.y+60})
        # Newly assembled craft give the player a full approach window.
        enemy.speed *= 0.48
        enemy.wave_amplitude *= 0.45
    if not assembly_story:
        assembly_story = true
        pending_dialogue.append_array([
            {"speaker":"MAX","text":"dlg.mars_4_2.assembly.max.001"},
            {"speaker":"ANDYGEN","text":"dlg.mars_4_2.assembly.andygen.002"},
            {"speaker":"MAX","text":"dlg.mars_4_2.assembly.max.003"}])

func find_wreck() -> Area2D:
    for unit in units:
        if is_instance_valid(unit) and unit.wreck and not unit.finished and unit.age < 6.0:
            return unit
    return null

func repair_warning() -> void:
    if warned:
        return
    warned = true
    pending_dialogue.append_array([
        {"speaker":"ROOK","text":"dlg.mars_4_2.repair.rook.001"},
        {"speaker":"ANDYGEN","text":"dlg.mars_4_2.repair.andygen.002"},
        {"speaker":"ROOK","text":"dlg.mars_4_2.repair.rook.003"}])

func fire_guard(guard: Area2D) -> void:
    var bullet := preload("res://scripts/enemy_bullet.gd").new()
    bullet.configure(guard.position+Vector2(0,35), (game.player.position-guard.position).normalized()*190.0)
    game.add_child(bullet)
