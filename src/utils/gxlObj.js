function getEdges(gxlObj) {
  return gxlObj.gxl.graph[0].edge.map((e) => ({
    from: e.$.from,
    x1: V.find((v) => v.id === e.$.from).x,
    y1: V.find((v) => v.id === e.$.from).y,
    x2: V.find((v) => v.id === e.$.to).x,
    y2: V.find((v) => v.id === e.$.to).y,
    to: e.$.to
  }));
}
function getVertices(gxlObj) {
  return  gxlObj.gxl.graph[0].node.map((n) => {
    const out = {};
    out.id = n.$.id;
    n.attr.forEach((v) => {
      out[v.$.name] = v.float[0];
    });
    return out;
  });
}
function getAdjMat(gxlObj) {
  const V = getVertices(gxlObj);
  const n = V.length;
  const E = getEdges(gxlObj);
  const mat = Array(n * n).fill(0);
  return E.forEach( e => {
    const i = V.findIndex( v => v.id === e.from);
    const j = V.findIndex( v => v.id === e.to);
    mat[n * i + j] = 1; mat[n * j + i] = 1;
  });
}
export { getVertices, getEdges, getAdjMat }