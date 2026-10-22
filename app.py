HTML

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Traffic Management System</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #eef4f8;
      margin: 0;
      color: #1d2939;
    }
    header {
      background: #12345a;
      color: white;
      text-align: center;
      padding: 22px 12px;
    }
    .container {
      max-width: 850px;
      margin: 20px auto;
      padding: 12px;
    }
    .card {
      background: white;
      padding: 18px;
      margin-bottom: 15px;
      border-radius: 12px;
      box-shadow: 0 2px 8px #0001;
    }
    button {
      background: #087e8b;
      color: white;
      border: none;
      border-radius: 7px;
      padding: 10px 15px;
      cursor: pointer;
    }
    .signal {
      background: #222;
      width: 65px;
      padding: 10px;
      border-radius: 12px;
      margin: 10px auto;
    }
    .light {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      margin: 7px auto;
      background: #555;
    }
    .red { background: red; }
    .yellow { background: yellow; }
    .green { background: limegreen; }
    .status { font-weight: bold; }
  </style>
</head>
<body>
  <header>
    <h1>Smart Traffic Management System</h1>
    <p>Smarter Roads, Safer Journeys</p>
  </header>

  <div class="container">

    <div class="card">
      <h2>1. Smart Traffic Signals</h2>
      <div class="signal">
        <div id="red" class="light red"></div>
        <div id="yellow" class="light"></div>
        <div id="green" class="light"></div>
      </div>
      <p id="signalStatus" class="status">Signal: STOP</p>
      <button onclick="changeSignal()">Change Signal</button>
    </div>

    <div class="card">
      <h2>2. Traffic Density Monitoring</h2>
      <p>Choose the traffic level:</p>
      <select id="density">
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
      <button onclick="checkDensity()">Check Traffic</button>
      <p id="densityResult">Traffic status will appear here.</p>
    </div>

    <div class="card">
      <h2>3. Emergency Vehicle Priority</h2>
      <p>Give priority to an ambulance or fire engine.</p>
      <button onclick="emergency()">Emergency Alert</button>
      <p id="emergencyResult">No emergency reported.</p>
    </div>

    <div class="card">
      <h2>4. Traffic Information</h2>
      <button onclick="showInfo()">Show Safety Tips</button>
      <p id="infoResult">Click to view traffic safety tips.</p>
    </div>

  </div>

  <script>
    let signal = 0;

    function changeSignal() {
      const lights = ["red", "green", "yellow"];
      document.getElementById("red").className = "light";
      document.getElementById("yellow").className = "light";
      document.getElementById("green").className = "light";

      signal = (signal + 1) % 3;
      const active = lights[signal];
      document.getElementById(active).className = "light " + active;

      const messages = {
        red: "STOP",
        green: "GO",
        yellow: "WAIT"
      };
      document.getElementById("signalStatus").textContent =
        "Signal: " + messages[active];
    }

    function checkDensity() {
      const level = document.getElementById("density").value;
      const advice = {
        Low: "Traffic is low. Roads are relatively clear.",
        Medium: "Moderate traffic. Drive carefully.",
        High: "Heavy traffic. Consider an alternate route."
      };
      document.getElementById("densityResult").textContent =
        advice[level];
    }

    function emergency() {
      document.getElementById("emergencyResult").textContent =
        "Emergency priority requested! In a real system, authorized traffic control is required.";
    }

    function showInfo() {
      document.getElementById("infoResult").textContent =
        "Follow traffic signals, wear a helmet or seat belt, avoid phone use while driving, and give way to emergency vehicles.";
    }
  </script>
</body>
</html>
