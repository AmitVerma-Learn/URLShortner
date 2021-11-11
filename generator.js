// This is a random 8 character generator in Javascript
<html>
<body>

<h2>8 character Random Generator</h2>
<p>We are using JavaScript Date.now() and to.String() functions</p>
<p>From Date.now() we take the current number of "milliseconds that elapsed since 1st January 1970 till this moment and using to.String(36) we convert it into a radix-36 representation.</p>

<p id="Rand8JS"></p>

<script>
document.getElementById("Rand8JS").innerHTML = Date.now().toString(36)
</script>

</body>
</html> 



