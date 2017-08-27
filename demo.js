function make_city(cityname, dom_id){
	achart = echarts.init(document.getElementById(dom_id));
	var option =  {
		"title": [
			{
				"textStyle": {
					"color": "#000", 
					"fontSize": 18
				}, 
				"subtext": "", 
				"text": cityname, 
				"top": "auto", 
				"subtextStyle": {
					"color": "#aaa", 
					"fontSize": 12
				}, 
				"left": "auto"
			}
		], 
		"legend": [
			{
				"selectedMode": "multiple",
				"top": "top",
				"orient": "horizontal",
				"data": [
					""
				],
				"left": "center",
				"show": true
			}
		],
		"backgroundColor": "#fff",
		"series": [
			{
				"mapType": cityname,
				"data": [],
				"name": "",
				"symbol": "circle",
				"type": "map",
				"roam": true
			}
		]
	};
	achart.setOption(option);	
}
