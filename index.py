a="""
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>DEVELOPED AS PART OF PROJECT BY NIMISH JINDAL, DELHI TECHNOLOGICAL UNIVERSITY</title>
	<meta name="keywords" content="" />
	<meta name="description" content="DEVELOPED AS PART OF PROJECT BY NIMISH JINDAL, DELHI TECHNOLOGICAL UNIVERSITY" />
	<link type="text/css" media="screen" rel="stylesheet" href="/static/style.css" />

	<meta name="viewport"    content="width=device-width, initial-scale=1.0">

	<!--link rel="shortcut icon" href="assets/images/gt_favicon.png"-->
	
	<!-- Bootstrap itself -->
	<link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet" type="text/css">

	<!-- Custom styles -->
	<!--link rel="stylesheet" href="assets/css/magister.css"-->

	<!-- Fonts -->
	<link href="http://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css" rel="stylesheet" type="text/css">
	<!--link href='http://fonts.googleapis.com/css?family=Wire+One' rel='stylesheet' type='text/css'-->
    
</head>

<body>

<div id="wrapper">

<!-- start menu -->
	 <!--div id="menu">
		<!--p>CRAWLED WEBSITE:<a href="https://www.udacity.com/cs101x/index.html/">UDACITY</a></p>
	 </div-->


<!-- start header -->
<div id="header" style="text-align:center;">
<font face="Cambria" color="#980000" size="8">Hybrid Recommender System</font><br>
<font face="calibri" color="#000555" size="3">1.Submit details (rate atleast 2 movies) &nbsp;&nbsp;2.To change a rating re-submit &nbsp;&nbsp;3.Get recommendations
</div>

<!-- start page -->
<div id="page" style="text-align:center;">
		<div id="content1">
			<table border="0" align="center" width=75%>
			<tr><td>Avengers</td>  <td>The Hangover</td>  <td>Bridesmaid</td>   <td>The Dark Knight</td>  <td>Horrible Bosses</td></tr>
			<tr><td>American Pie</td>  <td>Iron Man</td>  <td>Avatar</td>  <td>Pride and Prejudice</td>  <td>Inception</td></tr>
			<tr><td>Sherlock Holmes</td>  <td>Life of Pie</td>  <td>The Illusionist</td>  <td>The Notebook</td><td>Fight Club</td></tr>
			<tr><td>Spider Man</td>  <td>Usual Suspects</td>  <td>The Hobbit</td>  <td>Twilight</td>  <td>Delhi Belly</td></tr>
			<tr><td>The Prestige</td>    <td>Skyfall</td>  <td>Titanic</td>  <td>Bourne Ultimatum</td>  <td>Harry Potter</td></tr>
			</table>
		</div>

		<div id="content2">
			<form action="/sub" method="post"><br>
			Name:       <input type='text'  name="u_name" size="30" value="username"> <br><br>
			Age:        <input type='text'  name="age" size="30" value="age in years"> <br><br>
			Sex: <input type="radio" name="sex" value="0" checked="checked">Male <input type="radio" name="sex" value="1">Female<br><br>
			Movie:       <input type='text'  name="m_name" size="30" value="from above list"> <br><br>
			Rating:      <input type='text'  name="rating" size="30" value="out of 5"><br><br>
			<input type="submit" value="Submit" style="font-face: 'Comic Sans MS';  color: black; border: 1pt ridge lightgrey">
			</form><hr>

			<form action="/sign" method="post">
			<input type='text'  name="u_name" size="15" value="user name">
			<input type="submit" value="View Profile" style="font-face: 'Comic Sans MS';  color: black; border: 1pt ridge lightgrey">
			</form>

			<form action="/recom" method="post">
			  <p><br>
			    <input type='text'  name="u_name" size="15" value="user name">
			    <input type="submit" value="Get Recommendations" style="font-face:'Comic Sans MS'; color:black; border:1pt ridge lightgrey">
		      </p>
			  <p>&nbsp;</p>
			</form>
		</div>
</div>

<!--start footer-->
 <div id="footer">
<a href="https://github.com/nnimish19?tab=repositories" target="_blank">
						<img width="32" height="32" title="" alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpFNTE3OEEyQTk5QTAxMUUyOUExNUJDMTA0NkE4OTA0RCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpFNTE3OEEyQjk5QTAxMUUyOUExNUJDMTA0NkE4OTA0RCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkU1MTc4QTI4OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkU1MTc4QTI5OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+m4QGuQAAAyRJREFUeNrEl21ojWEYx895TDPbMNlBK46IUiNmPvHBSUjaqc0H8pF5+aDUKPEBqU2NhRQpX5Rv5jWlDIWlMCv7MMSWsWwmb3tpXub4XXWdPHvc9/Gc41nu+nedc7/8r/99PffLdYdDPsvkwsgkTBwsA/PADJCnzX2gHTwBt8Hl7p537/3whn04XoDZDcpBlk+9P8AFcAghzRkJwPF4zGGw0Y9QS0mAM2AnQj77FqCzrtcwB1Hk81SYojHK4DyGuQ6mhIIrBWB9Xm7ug/6B/nZrBHBegrkFxoVGpnwBMSLR9EcEcC4qb8pP14BWcBcUgewMnF3T34VqhWMFkThLJAalwnENOAKiHpJq1FZgI2AT6HZtuxZwR9GidSHtI30jOrbawxlVX78/AbNfhHlomEUJJI89O2MqeE79T8/nk8nMBm/dK576hZgmA3cp/R4l9/UeSxiHLVIlNm4nFfT0bxyuIj7LHRTKai+zdJobwMKzcZSJb0ePV5PKN+BqAAKE47UlMnERELMM3EdYP/yrd+XYb2mOiYBiQ8OQnoRBlXrl9JZix7D1pHTazu4MoyBcnYamqAjIMTR8G4FT8LuhLsexXYYjICBiqhQBvYb6fLZIJCjPypVvaOoVAW2WcasCnL2Nq82xHJNSqlCeFcDshaPK0twkAhosjZL31QYw+1rlMpWGMArl23SBsZZO58F2tlJXmjOXS+s4WGvpMiBJT/I2PInZ6lIs9/hBsNS1hS6BG0DSqmYEDRlCXQrmy50P1oDRKTSegmNbUsA0zDMwRhPJXeCE3vWLPQMvan6X8AgIa1vcR4AkGZkDR4ejJ1UHpsaVI0g2LInpOsNFUud1rhxSV+fzC9Woz2EZkWQuja7/B+jUrgtIMpy9YCW4n4K41YfzRneW5E1KJTe4B2Zq1Q5EHEtj4U3AfEzR5SVY4l7QYQPJdN2as7RKBF0BPZqqH4VgMAMBL8Byxr7y8zCZiDlnOcEKIPmUpgB5Z2ww5RdOiiRiNajUmWda5IG6WbhsyY2fx6m8gLcoJDJFkH219M3We1+cnda93pfycZpIJEL/s/wSYADmOAwAQgdpBAAAAABJRU5ErkJggg==" />
						Fork on Github</a></p>
       <!--p id="legal">(c) 2014 Developed as part of project.</p-->
</div>
</font>
</div>
</body>
</html>
"""
