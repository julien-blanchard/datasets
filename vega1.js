function getPlot(plotLocation) {
  let spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
  "width": 400,
  "height": 250,
  "config": {"axis": {"grid": false}, "view": {"strokeWidth":0},"font":"verdana", "background":"white"},
  "title": {"text":"Top primary categories", "anchor":"start"},
  "description": "Pokemon dataset visualiszation",
  "data": {"url": "https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv"},
  "mark": {"type":"bar", "tooltip": true},
  "encoding": {
    "x": {"field": "Attack", "aggregate": "mean", "title": "Volume"},
    "y": {"field": "Primary", "type": "nominal", "sort":"-x"},
    "color": {"field": "Attack", "aggregate": "mean", "title": "Volume", "scale": {"scheme": "yellowgreenblue"}}
    }
  }
  vegaEmbed(plotLocation, spec, {})
};

function getBarPlot(plotLocation) {
  let spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
  "width": 400,
  "height": 250,
  "config": {"axis": {"grid": false}, "view": {"strokeWidth":0},"font":"verdana", "background":"white"},
  "title": {"text":"Top primary types", "anchor":"start"},
  "description": "Pokemon dataset visualiszation",
  "data": {"url": "https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv"},
  "mark": {"type":"bar", "tooltip": true},
   "encoding": {
    "x": {"field": "Attack", "aggregate": "mean", "title": "Volume"},
    "y": {"field": "Primary", "type": "nominal"},
    "color": {"field":"Generation","type":"nominal", "sort":"descending", "scale": {"scheme": "yellowgreenblue"}}
    }
  }
  vegaEmbed(plotLocation, spec, {})
};

function getScatterrPlot(plotLocation) {
  let spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
  "width": 400,
  "height": 250,
  "config": {"axis": {"grid": false}, "view": {"strokeWidth":0},"font":"verdana", "background":"white"},
  "title": {"text":"Relationship between attack and defense", "anchor":"start"},
  "description": "Pokemon dataset visualiszation",
  "data": {"url": "https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv"},
  "mark": {"type":"point", "tooltip": true},
   "encoding": {
    "x": {"field": "Attack", "type":"quantitative", "title": "Volume"},
    "y": {"field": "Defense", "type": "quantitative"},
    "color": {"field":"Generation","type":"nominal", "scale": {"scheme": "yellowgreenblue"} },
    "size": {"field":"Generation","type":"nominal"}
    }
  }
  vegaEmbed(plotLocation, spec, {})
};

function getLinePlot(plotLocation) {
  let spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
  "width": 400,
  "height": 250,
  "config": {"axis": {"grid": false}, "view": {"strokeWidth":0},"font":"verdana", "background":"white"},
  "title": {"text":"Relationship between attack and defense", "anchor":"start"},
  "description": "Pokemon dataset visualiszation",
  "data": {"url": "https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv"},
  "mark": {"type":"line", "tooltip": true},
   "encoding": {
    "x": {"field": "Attack", "type":"quantitative", "title": "Volume"},
    "y": {"field": "Defense", "type": "quantitative"},
    "color": {"field": "Defense", "type": "quantitative", "scale": {"scheme": "yellowgreenblue"}}
    }
  }
  vegaEmbed(plotLocation, spec, {})
};
