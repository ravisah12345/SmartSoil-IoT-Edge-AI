
%% === CHANNEL CONFIGURATION ===
mainChannel  = 3200558;
alertChannel = 3203164;

readKey  = 'YOUR_READ_KEY_HERE';
writeKey = 'YOUR_WRITE_KEY_HERE';

%% === READ LATEST DATA ===
[data, ts] = thingSpeakRead(mainChannel, ...
    'NumPoints', 1, ...
    'OutputFormat','table');

%% === EXTRACT DATA ===
soil  = data.SoilMoisture;
temp  = data.Temperature;
hum   = data.Humidity;
light = data.Light;
ph    = data.PhLevel;
aiRaw = data.AiPrediction;   % RAW AI value (number or text)
soil2 = data.soil2;

%% =========================================================
%  AI PREDICTION CONVERSION (NUMBER → WORD)  ⭐ FIX ⭐
% =========================================================
if isnumeric(aiRaw)
    if aiRaw == 0
        aiText = "BAD";
    elseif aiRaw == 1
        aiText = "MODERATE";
    else
        aiText = "GOOD";
    end
else
    aiText = upper(string(aiRaw)); % Already text
end

%% === TREND SMOOTHING ===
soilHist = thingSpeakRead(mainChannel, 'Fields', 1, 'NumPoints', 3);
soilSmooth = mean(soilHist, 'omitnan');

humHist = thingSpeakRead(mainChannel, 'Fields', 3, 'NumPoints', 3);
humSmooth = mean(humHist, 'omitnan');

%% === READ PREVIOUS ALERT ===
prevAlert = thingSpeakRead(alertChannel, 'Fields', 1, 'NumPoints', 1);

if isempty(prevAlert)
    prevAlert = -1;   % Startup
end

%% =========================================================
%  SYSTEM STARTUP NOTIFICATION (ONCE)
% =========================================================
if prevAlert == -1
    alertLevel = 0;

    thingSpeakWrite(alertChannel, ...
        [alertLevel, soil, temp, hum, light, ph, aiText, soil2], ...
        'Fields', [1 2 3 4 5 6 7 8], ...
        'WriteKey', writeKey);

    pause(20);
    return;
end
