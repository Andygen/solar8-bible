extends Node2D

const SCAN_SECONDS := 22.0
const ENDING = [
    "LENA\n\ndlg.mars_4_4.result.lena.001",
    "MAX\n\ndlg.mars_4_4.result.max.002",
    "MAX\n\ndlg.mars_4_4.result.max.003",
    "VALE\n\ndlg.mars_4_4.ending.vale.001",
    "ANDYGEN\n\ndlg.mars_4_4.ending.andygen.002",
    "VALE\n\ndlg.mars_4_4.ending.vale.003",
]
const TRANSMISSIONS = [
    {"at":0.0,"speaker":"ROOK","text":"dlg.mars_4_4.discovery.rook.001"},
    {"at":5.0,"speaker":"MAX","text":"dlg.mars_4_4.discovery.max.002"},
]
const DEBRIEF = "All three samples survived. Max recovered a complete block of foreign code: compatible with SOLAR, but not designed by a human system. Vale restricted access to command clearance."
var game: Node2D
var nodes: Array[Area2D] = []
var phase := "approach"
var scanned := 0
var node_damage := 0
var cleared := false
var wave_clock := 0.0
var waves := 0
var dialogue_clock := 0.0
var pending_dialogue: Array[Dictionary] = []
var status: Label

func _ready() -> void:
    game = get_parent()
    for i in range(3):
        var sample := preload("res://scripts/missions/template_sample.gd").new()
        sample.controller = self
        sample.number = i
        sample.position = Vector2(game.viewport_size.x*[0.22,0.5,0.78][i],game.viewport_size.y*[0.58,0.49,0.58][i])
        add_child(sample)
        nodes.append(sample)
    status = Label.new()
    status.position = Vector2(24,180)
    status.size = Vector2(game.viewport_size.x-48,65)
    status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    status.add_theme_font_size_override("font_size",18)
    status.modulate = Color("83dde9")
    add_child(status)
    game.rook_companion.scan_completed.connect(_scan_completed)
    game.rook_companion.movement_speed = 180

func scan_id() -> String:
    return "foreign_sample_"+str(scanned)

func _process(delta: float) -> void:
    if game.game_over or cleared:
        return
    var rook = game.rook_companion
    if phase == "approach":
        status.text = "HIDDEN MODULE / PRESERVE ALL THREE SAMPLES"
        if game.elapsed >= 12:
            start_scan()
    elif phase == "scanning":
        status.text = tr("ROOK SCANNING %s / DEFEND ALL SAMPLES") % char(65+scanned)
        wave_clock -= delta
        if wave_clock <= 0:
            spawn_wave()
            wave_clock = 10.0
    elif phase == "extraction":
        status.text = "THREE SCANS COMPLETE / CLEAR DEFENDERS / ROOK RETURNING"
        if rook.state == rook.State.DOCKED and get_tree().get_nodes_in_group("enemies").is_empty():
            cleared = true
            phase = "saved"
            rook.movement_speed = 950
            rook.undock()
    dialogue_clock -= delta
    if not pending_dialogue.is_empty() and dialogue_clock <= 0:
        var line: Dictionary = pending_dialogue.pop_front()
        game.hud.show_transmission(line.speaker,line.text,2,4.5)
        dialogue_clock = 5

func start_scan() -> bool:
    if scanned >= 3 or game.game_over or nodes[scanned].hp <= 0:
        return false
    if not game.rook_companion.begin_scan(scan_id(),nodes[scanned].position,SCAN_SECONDS,tr("SAMPLE %s") % char(65+scanned),true,nodes[scanned]):
        return false
    phase = "scanning"
    return true

func _scan_completed(id: String) -> void:
    if phase != "scanning" or id != scan_id() or game.game_over:
        return
    nodes[scanned].scanned = true
    scanned += 1
    if scanned == 1:
        pending_dialogue.append_array([
            {"speaker":"MAX","text":"dlg.mars_4_4.scan_one.max.001"},
            {"speaker":"LENA","text":"dlg.mars_4_4.scan_one.lena.002"},
            {"speaker":"MAX","text":"dlg.mars_4_4.scan_one.max.003"},
        ])
    if scanned < 3:
        start_scan()
    else:
        phase = "extraction"
        game.rook_companion.dock()

func spawn_wave() -> void:
    # Each completed scan increases the number of attackers in the next wave.
    for i in range(scanned+1):
        var target := (waves+i)%3
        game._spawn_enemy_job({"kind":"striker" if scanned == 2 and i == 0 else "scout","x":nodes[target].position.x,"y":-80-i*80,"node_index":target})
        game.total_targets += 1
    waves += 1

func warn_under_attack() -> void:
    # The health flash and persistent labels show which sample needs cover.
    pass

func fail_defense() -> void:
    if game.game_over:
        return
    phase = "failed"
    game.rook_companion.cancel_scan(scan_id())
    game.game_over = true
    game.call_deferred("_show_result_panel",false)
