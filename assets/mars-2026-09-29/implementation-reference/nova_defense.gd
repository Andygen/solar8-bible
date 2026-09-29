extends Node2D

const SCAN_ID := "nova_isolated_partition"
const SCAN_SECONDS := 60.0
const ENDING = ["MAX\n\ndlg.mars_4_3.ending.max.001", "ANDYGEN\n\ndlg.mars_4_3.ending.andygen.002", "MAX\n\ndlg.mars_4_3.ending.max.003"]
const DEBRIEF = "NOVA's physical nodes survived. Max saved a small, isolated fragment of its clean personality. Two competing command processes remain inside the industrial network."
const TRANSMISSIONS = [
    {"at":0.0,"speaker":"ROOK","text":"dlg.mars_4_3.isolation.rook.001"},
    {"at":5.0,"speaker":"LENA","text":"dlg.mars_4_3.isolation.lena.002"},
    {"at":10.0,"speaker":"NOVA","text":"dlg.mars_4_3.contact.nova.001"},
    {"at":16.0,"speaker":"ANDYGEN","text":"dlg.mars_4_3.contact.andygen.002"},
    {"at":20.0,"speaker":"ROOK","text":"dlg.mars_4_3.contact.rook.003"},
]
var game: Node2D
var nodes: Array[Area2D] = []
var phase := "isolation"
var service_isolated := false
var fragment_saved := false
var cleared := false
var node_damage := 0
var defense_time := 0.0
var next_wave := 0
var clean_pulse_seen := false
var warned := false
var pending_dialogue: Array[Dictionary] = []
var dialogue_clock := 0.0
var status: Label

func _ready() -> void:
    game = get_parent()
    for i in range(3):
        var node := preload("res://scripts/missions/nova_node.gd").new()
        node.controller = self
        node.number = i
        node.position = Vector2(game.viewport_size.x*[0.22,0.5,0.78][i],game.viewport_size.y*0.59)
        add_child(node)
        nodes.append(node)
    status = Label.new()
    status.position = Vector2(24,160)
    status.size = Vector2(game.viewport_size.x-48,65)
    status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    status.add_theme_font_size_override("font_size",18)
    status.modulate = Color("83dde9")
    add_child(status)
    game.rook_companion.scan_completed.connect(_scan_completed)
    game.rook_companion.movement_speed = 180

func _process(delta: float) -> void:
    if game.game_over or cleared:
        return
    var rook = game.rook_companion
    if phase == "isolation":
        status.text = "ISOLATING SERVICE INTERFACE / FLIGHT CONTROL SEPARATE"
        if game.elapsed >= 24:
            service_isolated = true
            start_defense()
    elif phase == "defense":
        defense_time += delta
        # Corrupted sectors interrupt the read, never the player's controls.
        rook.scan_paused = fmod(defense_time,22.0) >= 18.0
        status.text = "CORRUPTED SECTOR / READ PAUSED / KEEP DEFENDING" if rook.scan_paused else "DEFEND THREE NODES / ROOK READING MEMORY"
        if next_wave < 9 and defense_time >= next_wave*8.0:
            spawn_wave()
            next_wave += 1
        if not clean_pulse_seen and rook.scan_fraction(SCAN_ID) >= 0.4:
            clean_pulse_seen = true
            pending_dialogue.append_array([
                {"speaker":"NOVA","text":"dlg.mars_4_3.pulse.nova.001"},
                {"speaker":"LENA","text":"dlg.mars_4_3.pulse.lena.002"},
                {"speaker":"NOVA","text":"dlg.mars_4_3.pulse.nova.003"}])
    elif phase == "extraction":
        status.text = "READ COMPLETE / CLEAR DEFENDERS / ROOK RETURNING"
        if rook.state == rook.State.DOCKED and get_tree().get_nodes_in_group("enemies").is_empty():
            fragment_saved = true
            cleared = true
            phase = "saved"
            rook.movement_speed = 950
            rook.undock()
    dialogue_clock -= delta
    if not pending_dialogue.is_empty() and dialogue_clock <= 0:
        var line: Dictionary = pending_dialogue.pop_front()
        game.hud.show_transmission(line.speaker,line.text,2,4.5)
        dialogue_clock = 5.0
    queue_redraw()

func start_defense() -> bool:
    if phase != "isolation" or not service_isolated:
        return false
    if not game.rook_companion.begin_scan(SCAN_ID,nodes[1].position,SCAN_SECONDS,"NOVA",true,nodes[1],true):
        return false
    phase = "defense"
    return true

func spawn_wave() -> void:
    for i in range(2):
        var index := (next_wave+i)%3
        game._spawn_enemy_job({"kind":"striker" if next_wave%3 == 2 else "scout","x":nodes[index].position.x,"y":-80-i*80,"node_index":index})
        game.total_targets += 1

func warn_under_attack() -> void:
    if warned:
        return
    warned = true
    game.hud.show_transmission("ROOK","dlg.mars_4_3.defense.rook.001",3,4.0)
    pending_dialogue.push_front({"speaker":"MAX","text":"dlg.mars_4_3.defense.max.002"})
    dialogue_clock = 4.5

func _scan_completed(id: String) -> void:
    if id != SCAN_ID or phase != "defense":
        return
    phase = "extraction"
    game.rook_companion.dock()

func fail_defense() -> void:
    if game.game_over:
        return
    phase = "failed"
    game.rook_companion.cancel_scan(SCAN_ID)
    game.game_over = true
    game.call_deferred("_show_result_panel",false)

func _draw() -> void:
    if nodes.size() < 3:
        return
    var color := Color(0.28,0.78,0.84,0.35)
    for index in [0,2]:
        draw_line(nodes[index].position,nodes[1].position,color,2,true)
