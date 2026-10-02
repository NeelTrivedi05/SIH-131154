Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.SetOutputToWaveFile("test_audio.wav")
$synth.Speak("Testing speech synthesis for PolarGrid AI.")
$synth.Dispose()
Write-Host "TTS_SUCCESS"
