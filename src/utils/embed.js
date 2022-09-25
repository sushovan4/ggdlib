function embedGraph(graph) {
    const out = JSON.parse(JSON.stringify(graph));
    const edges = getEdges(out);
    for (let i = 0; i < edges.length; i++)
      for (let j = i + 1; j < edges.length; j++) {
        if (
          edges[i].from === edges[j].from ||
          edges[i].from === edges[j].to ||
          edges[i].to === edges[j].from ||
          edges[i].to === edges[j].to
        )
          continue;
        const point = intersection(edges[i], edges[j]);
        if (point !== null) {
          const nodes = out.gxl.graph[0].node;
          const id = nodes.length;
          nodes.push({
            $: { id: "_" + nodes.length },
            attr: [
              { $: { name: "x" }, float: [point.x + ""] },
              { $: { name: "y" }, float: [point.y + ""] }
            ]
          });
          out.gxl.graph[0].edge.splice(i, 1);
          out.gxl.graph[0].edge.splice(j - 1, 1);
          out.gxl.graph[0].edge.push({
            $: { from: edges[i].from, to: "_" + id }
          });
          out.gxl.graph[0].edge.push({
            $: { from: "_" + id, to: edges[i].to }
          });
          out.gxl.graph[0].edge.push({
            $: { from: edges[j].from, to: "_" + id }
          });
          out.gxl.graph[0].edge.push({
            $: { from: "_" + id, to: edges[j].to }
          });
          console.log(out, i, j, point);
          return embedGraph(out);
        }
      }
    return out;
  }
function intersection(e, f) {
    let det, gamma, lambda;
    let a = parseFloat(e.x1),
      b = parseFloat(e.y1),
      c = parseFloat(e.x2),
      d = parseFloat(e.y2);
    let p = f.x1,
      q = f.y1,
      r = f.x2,
      s = f.y2;
    det = (c - a) * (s - q) - (r - p) * (d - b);
    if (det !== 0) {
      lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
      gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
      if (0 < lambda && lambda < 1 && 0 < gamma && gamma < 1)
        return {x: a + lambda * (c - a), y: b + lambda * (d - b)};
    }
    return null;
  }
