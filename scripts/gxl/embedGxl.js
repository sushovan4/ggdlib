import { edges } from "./gxlObj";

function embedObj(gxlObj) {
  const out = JSON.parse(JSON.stringify(gxlObj));
  const edges = edges(out);

  for (let i = 0; i < edges.length; i++)
    for (let j = i + 1; j < edges.length; j++) {
      if (
        edges[i].from === edges[j].from ||
        edges[i].from === edges[j].to ||
        edges[i].to === edges[j].from ||
        edges[i].to === edges[j].to
      ) continue;

      const e = edges[i], f = edges[j];
      const point = intersection(e, f);
      if (point === null) continue;

      const nodes = out.gxl.graph[0].node;
      const id = "_" + nodes.length;
      nodes.push({
      $: { id: id },
        attr: [
          { $: { name: "x" }, float: [point.x + ""] },
          { $: { name: "y" }, float: [point.y + ""] }
        ]
      });
      
      out.gxl.graph[0].edge.splice(i, 1);
      out.gxl.graph[0].edge.splice(j - 1, 1);

      out.gxl.graph[0].edge.push({
        $: { from: e.from, to: id }
      });
      out.gxl.graph[0].edge.push({
        $: { from: id, to: e.to }
      });

      out.gxl.graph[0].edge.push({
        $: { from: f.from, to: id }
      });
      out.gxl.graph[0].edge.push({
        $: { from: id, to: f.to }
      });
      return embedObj(out);
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
  if (Math.abs(det) > 1e-10) {
      lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
      gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
      if (0.001 < lambda && lambda < 0.999 && 0.001 < gamma && gamma < 0.999) {
        return {x: a + lambda * (c - a), y: b + lambda * (d - b)};
      }
  }
  return null;
}
export { embedObj };