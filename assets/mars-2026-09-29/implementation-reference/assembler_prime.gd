extends Node2D

const ENDING = ["SOLAR\n\ndlg.mars_4_5.ending.solar.001","ANDYGEN\n\ndlg.mars_4_5.ending.andygen.002","ROOK\n\ndlg.mars_4_5.ending.rook.003","MAYA\n\ndlg.mars_4_5.ending.maya.004","ROOK\n\ndlg.mars_4_5.ending.rook.005"]
const DEBRIEF = "Assembler Prime's foreign control module was scanned and destroyed. A clean SOLAR fragment broke through, then vanished. The next relay vector leads to Jupiter."
const TRANSMISSIONS = [
    {"at":0.0,"speaker":"MAX","text":"dlg.mars_4_5.reveal.max.001"},
    {"at":4.5,"speaker":"ANDYGEN","text":"dlg.mars_4_5.reveal.andygen.002"},
    {"at":9.0,"speaker":"MAX","text":"dlg.mars_4_5.reveal.max.003"},
    {"at":13.5,"speaker":"ROOK","text":"dlg.mars_4_5.production.rook.001"},
]
var game: Node2D
var rig: Node2D
var phase := 1
var phase_age := 0.0
var age := 0.0
var opening := 0.0
var arms: Array[Area2D] = []
var repairs: Array[Area2D] = []
var armor: Area2D
var core: Area2D
var defeated := false
var transition_pending := false
var scan_started := false
var scan_done := false
var armor_restored := 0
var mechanical_hits := 0
var attack_clock := 0.0
var repair_clock := 0.0
var wave_clock := 0.0
var slam_age := -1.0
var slam_x := 0.0
var slam_arm := 0
var slam_hit := false
var status: Label
var pending_dialogue: Array[Dictionary] = []
var dialogue_clock := 0.0

func _ready() -> void:
    game = get_parent()
    rig = preload("res://scripts/visual/assembler_rig.gd").new()
    rig.position = Vector2(game.viewport_size.x*0.5,game.viewport_size.y*0.39)
    rig.scale = Vector2.ONE*game.viewport_size.x/1100.0
    add_child(rig)
    for i in range(4):
        var target := _target("arm",16,Vector2.ZERO)
        target.number = i
        arms.append(target)
    _position_arms()
    status = Label.new()
    status.position = Vector2(24,230)
    status.size = Vector2(game.viewport_size.x-48,66)
    status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    status.add_theme_font_size_override("font_size",18)
    status.modulate = Color("ffcf98")
    add_child(status)
    game.boss_spawned = true
    game.boss_started_at = game.elapsed
    game.get_node("/root/MenuMusic").intensify_mission()
    game.rook_companion.scan_completed.connect(_scan_completed)

func _target(kind: String, hp: int, point: Vector2) -> Area2D:
    var target := preload("res://scripts/bosses/assembler_target.gd").new()
    target.controller = self
    target.kind = kind
    target.hp = hp
    target.maximum = hp
    target.position = point
    add_child(target)
    return target

func _position_arms() -> void:
    for i in range(arms.size()):
        arms[i].position = rig.position+rig.wrists[i]*rig.scale

func arms_left() -> int:
    return arms.filter(func(target): return not target.dead).size()

func repairs_left() -> int:
    return repairs.filter(func(target): return not target.dead).size()

func target_disabled(target: Area2D) -> void:
    var burst := preload("res://scripts/vfx/explosion.gd").new()
    burst.position = target.position
    burst.configure(0.7 if target.kind != "core" else 2.5,Color("ffb46c"),Color.WHITE)
    game.add_child(burst)
    if target.kind == "arm":
        rig.disable_arm(target.number)
        if slam_age >= 0 and slam_arm == target.number:
            slam_age = -1
        if arms_left() == 0 and not transition_pending:
            transition_pending = true
            call_deferred("_enter_phase",2)
    elif target.kind == "armor" and not transition_pending:
        transition_pending = true
        call_deferred("_enter_phase",3)
    elif target.kind == "core":
        defeated = true
        game.boss_defeated = true
        game.boss_fight_duration = game.elapsed-game.boss_started_at
        game.score += 10000
        rig.modulate = Color(0.25,0.25,0.25)
        rig.sprites.core.hide()
        core.hide()
        status.text = "FOREIGN MODULE DESTROYED / CLEAR REMAINING DRONES"
        game.boss_bar.value = 0
    elif target.kind == "repair":
        target.modulate = Color(0.25,0.25,0.25)

func _enter_phase(next_phase: int) -> void:
    if game.game_over or defeated:
        return
    transition_pending = false
    phase = next_phase
    game.boss_phase = phase
    phase_age = 0
    attack_clock = 0
    repair_clock = 0
    wave_clock = 0
    slam_age = -1
    pending_dialogue.clear()
    dialogue_clock = 0
    if phase == 2:
        armor = _target("armor",60,rig.position+Vector2(0,-30))
        for side in [-1,1]:
            repairs.append(_target("repair",12,rig.position+Vector2(side*130,105)))
        pending_dialogue.append_array([
            {"speaker":"ROOK","text":"dlg.mars_4_5.repair.rook.001"},
            {"speaker":"ANDYGEN","text":"dlg.mars_4_5.repair.andygen.002"},
        ])
    elif phase == 3:
        armor.hide()
        core = _target("core",42,rig.position+Vector2(0,-45)*rig.scale)
        # A short protected acquisition period makes the mandatory scan compatible
        # with automatic player fire. Its five seconds begin after Andygen's line.
        pending_dialogue.append_array([
            {"speaker":"ROOK","text":"dlg.mars_4_5.core.rook.001"},
            {"speaker":"MAX","text":"dlg.mars_4_5.core.max.002"},
            {"speaker":"ANDYGEN","text":"dlg.mars_4_5.core.andygen.003"},
            {"speaker":"MAX","text":"dlg.mars_4_5.core.max.004"},
        ])

func _process(delta: float) -> void:
    if game.game_over or defeated:
        return
    age += delta
    phase_age += delta
    attack_clock += delta
    wave_clock += delta
    var desired_opening := 0.0 if phase == 1 else (35.0 if phase == 2 else 98.0)
    opening = move_toward(opening,desired_opening,delta*150)
    rig.pose(age,opening)
    _position_arms()
    if phase == 1:
        status.text = tr("DISABLE MANIPULATORS / %d LEFT") % arms_left()
        if phase_age >= 18:
            if wave_clock >= 12:
                wave_clock = 0
                _wave()
            if attack_clock >= 5 and slam_age < 0:
                attack_clock = 0
                _start_slam()
        _slam(delta)
    elif phase == 2:
        status.text = tr("REPAIR MODULES %d / STOP ARMOR REGENERATION") % repairs_left()
        repair_clock += delta
        if repair_clock >= 2:
            repair_clock = 0
            var healed := mini(armor.maximum-armor.hp,repairs_left()*3)
            armor.hp += healed
            armor_restored += healed
        if phase_age >= 5 and attack_clock >= 3.2:
            attack_clock = 0
            _fan(5,210)
    elif phase == 3:
        if phase_age >= 11 and not scan_started:
            scan_started = game.rook_companion.begin_scan("assembler_core",core.position,5,tr("MAX / CORE SCAN"),false,core)
        status.text = "CORE SHIELDED / MAX PREPARING SCAN"
        if scan_started:
            status.text = "SCAN COMPLETE / DESTROY FOREIGN MODULE" if scan_done else tr("MAX SCANNING / CORE PROTECTED / %02d%%") % int(game.rook_companion.scan_fraction("assembler_core")*100)
        if phase_age >= 4 and attack_clock >= 2.8:
            attack_clock = 0
            _fan(7,230)
    dialogue_clock -= delta
    if not pending_dialogue.is_empty() and dialogue_clock <= 0:
        var line: Dictionary = pending_dialogue.pop_front()
        game.hud.show_transmission(line.speaker,line.text,2,4.5)
        dialogue_clock = 5
    _update_bar()
    queue_redraw()

func _scan_completed(id: String) -> void:
    if id == "assembler_core" and phase == 3 and not game.game_over:
        scan_done = true

func _wave() -> void:
    if get_tree().get_nodes_in_group("enemies").size() >= 4:
        return
    for side in [-1,1]:
        game._spawn_enemy_job({"kind":"scout","x":rig.position.x+side*90,"y":rig.position.y+150})
        game.total_targets += 1

func _fan(count: int, speed: float) -> void:
    var origin := rig.position+Vector2(0,120)
    var direction: Vector2 = (game.player.position-origin).normalized()
    for i in range(count):
        var bullet := preload("res://scripts/enemy_bullet.gd").new()
        bullet.configure(origin,direction.rotated((i-(count-1)*0.5)*0.19)*speed)
        game.add_child(bullet)

func _start_slam() -> void:
    for offset in range(1,5):
        var index := (slam_arm+offset)%4
        if not arms[index].dead:
            slam_arm = index
            break
    slam_x = game.player.position.x
    slam_age = 0
    slam_hit = false

func _slam(delta: float) -> void:
    if slam_age < 0:
        return
    slam_age += delta
    var in_lane: bool = absf(game.player.position.x-slam_x)<34 and game.player.position.y >= rig.position.y+160 and game.player.position.y <= game.viewport_size.y-100
    if slam_age >= 1.5 and slam_age < 1.85 and not slam_hit and in_lane and game.player.invulnerable <= 0:
        slam_hit = true
        mechanical_hits += 1
        game.player.take_damage(1)
    if slam_age >= 1.85:
        slam_age = -1

func _update_bar() -> void:
    game.boss_label.show()
    game.boss_bar.show()
    game.boss_label.text = tr("ASSEMBLER PRIME / PHASE %d") % phase
    if phase == 1:
        game.boss_bar.max_value = 64
        game.boss_bar.value = arms.reduce(func(total,target): return total+target.hp,0)
    elif phase == 2:
        game.boss_bar.max_value = armor.maximum
        game.boss_bar.value = armor.hp
    else:
        game.boss_bar.max_value = core.maximum
        game.boss_bar.value = core.hp

func _draw() -> void:
    if phase == 1 and phase_age >= 16 and wave_clock >= 10 and not defeated:
        for side in [-1,1]:
            var port := rig.position+Vector2(side*90,150)
            draw_arc(port,30,-PI/2,-PI/2+TAU*clampf((wave_clock-10)/2,0,1),40,Color("ffcc77"),3,true)
    if slam_age >= 0 and not defeated:
        var active := slam_age >= 1.5
        var color := Color(1,0.18,0.04,0.8) if active else Color(1,0.65,0.2,0.28)
        draw_line(arms[slam_arm].position,Vector2(slam_x,rig.position.y+160),color,5 if active else 1,true)
        draw_line(Vector2(slam_x,rig.position.y+160),Vector2(slam_x,game.viewport_size.y-100),color,68 if active else 2,true)
        if not active:
            for side in [-1,1]:
                draw_line(Vector2(slam_x+side*34,rig.position.y+160),Vector2(slam_x+side*34,game.viewport_size.y-100),color,2,true)
