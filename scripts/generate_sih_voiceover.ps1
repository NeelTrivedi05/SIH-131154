# generate_sih_voiceover.ps1
# Synthesizes full voiceover audio for the 3-minute SIH submission video

$audioDir = "sih_video_3min/audio"
if (!(Test-Path $audioDir)) {
    New-Item -ItemType Directory -Path $audioDir -Force | Out-Null
}

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0

$voices = $synth.GetInstalledVoices()
Write-Host "Installed Voices:"
foreach ($v in $voices) {
    Write-Host " - $($v.VoiceInfo.Name)"
}

$preferred = $voices | Where-Object { $_.VoiceInfo.Name -match "David|Zira|Mark|George" } | Select-Object -First 1
if ($preferred) {
    $synth.SelectVoice($preferred.VoiceInfo.Name)
    Write-Host "Selected Voice: $($preferred.VoiceInfo.Name)"
}

$scene1Text = "India's Antarctic stations, Maitri and Bharati, operate under some of the most unforgiving conditions on Earth, with temperatures plunging to minus 50 degrees Celsius and winds exceeding 100 kilometers per hour. Currently, these stations rely heavily on diesel fuel, shipped once a year by icebreakers. Running generators inefficiently leads to wet-stacking damage and wasted fuel. To solve Problem Statement SIH26061, we present PolarGrid AI: a physics-grounded digital twin and advisory decision support system designed to maximize polar renewable utilization while guaranteeing 100 percent life-support reliability."

$scene2Text = "Accurate dispatch begins with predictive forecasting. Rather than making unsubstantiated claims, we benchmarked a Scikit-Learn Ridge regression model against a 24-hour persistence baseline across an 80-20 chronological split. Our model achieved an empirical test MAE of 1.75 kilowatts compared to 2.96 kilowatts for the baseline, a 40.9 percent improvement. This gives station operators foresight to pre-charge batteries before polar storms hit."

$scene3Text = "Our dashboard is backed by a full digital twin. In our Summer Maximum scenario, 24-hour sunlight yields over 55 percent renewable penetration, with surplus power automatically directed to charge the 150 kilowatt-hour battery bank. Notice how smoothly the system recalculates in real-time as we adjust parameters like wind speed and battery capacity. In Polar Night, solar output drops to zero, and the system seamlessly advises battery buffering and generator scheduling."

$scene4Text = "Here is where real engineering matters. In our Blizzard scenario, wind speeds surge above 25 meters per second. Instead of unrealistically claiming infinite wind power, PolarGrid AI models aerodynamic storm furling: the blades automatically feather to prevent catastrophic mechanical failure, cutting wind power to zero. The system immediately fires a critical safety interlock alert. Furthermore, notice our genset dispatch: to prevent cylinder bore glazing and engine wet-stacking, our algorithm enforces a strict 55 percent minimum loading clamp, meaning our 120 kilowatt generator never idles below 66 kilowatts. Any excess generation is diverted into battery storage."

$scene5Text = "Under extreme deficits, our 3-tier shedding relay protects Tier 1 Life Support and Medical heating at all costs, shedding non-essential auxiliary loads first. For fuel savings, we rejected the common flaw of comparing against an unrealistic all-diesel baseline. Instead, we measure against a realistic rule-based heuristic policy, demonstrating a verified 8 to 16 percent seasonal fuel reduction, saving 18,000 to 38,000 liters of Antarctic diesel annually. All hourly telemetry can be exported directly to CSV for MoES compliance. PolarGrid AI is ready to deploy offline, runs on zero cloud dependencies, and brings scientific rigor to polar clean energy transition."

$scenes = @(
    @{ id = "scene_1"; text = $scene1Text },
    @{ id = "scene_2"; text = $scene2Text },
    @{ id = "scene_3"; text = $scene3Text },
    @{ id = "scene_4"; text = $scene4Text },
    @{ id = "scene_5"; text = $scene5Text }
)

foreach ($s in $scenes) {
    $outPath = Join-Path $audioDir "$($s.id).wav"
    Write-Host "Synthesizing $($s.id)..."
    $synth.SetOutputToWaveFile($outPath)
    $synth.Speak($s.text)
    Write-Host "Saved: $outPath"
}

$synth.Dispose()
Write-Host "ALL_VOICEOVERS_GENERATED"
