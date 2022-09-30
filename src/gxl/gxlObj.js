function edges(gxlObj) {
  const V = vertices(gxlObj);
  if(!gxlObj.gxl.graph[0].edge)
    return [];
  return  gxlObj.gxl.graph[0].edge.map((e) => ({
    from: e.$.from,
    x1: V.find((v) => v.id === e.$.from).x,
    y1: V.find((v) => v.id === e.$.from).y,
    x2: V.find((v) => v.id === e.$.to).x,
    y2: V.find((v) => v.id === e.$.to).y,
    to: e.$.to
  }));
}
function vertices(gxlObj) {
  return  gxlObj.gxl.graph[0].node.map((n) => {
    const out = {};
    out.id = n.$.id;
    n.attr.forEach((v) => {
      out[v.$.name] = v.float[0];
    });
    return out;
  });
}
function adjMat(gxlObj) {
  const V = vertices(gxlObj);
  const n = V.length;
  const E = edges(gxlObj);
  const mat = Array(n * n).fill(0);
  V.forEach( (v, i) => mat[n * i + i] = [v.x, v.y]);
  E.forEach( e => {
    const i = V.findIndex( v => v.id === e.from);
    const j = V.findIndex( v => v.id === e.to);
    mat[n * i + j] = 1; mat[n * j + i] = 1;
  });
  return mat;
}

export { vertices, edges, adjMat };