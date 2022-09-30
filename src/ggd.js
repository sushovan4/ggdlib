function ggd(adjMat1, adjMat2, C_V = 0.5, C_E = 1, i = 0, j = -1, 
  pi = Array(Math.sqrt(adjMat1.length))) {
  const m = Math.sqrt(adjMat1.length), n = Math.sqrt(adjMat2.length);

  if(i === m) {
    let cost = 0;
    pi.forEach( (j, i)  => {
      // vertex translation
      if(j !== -1)
        cost = cost + C_V * dist(adjMat1[m * i + i], adjMat2[n * j + j]);
    });
    for (let i = 0; i < m; i++)
      for (let j = i + 1; j < m; j++) {
        if (adjMat1[m * i + j] === 1)
          if (pi[i] === -1 || pi[j] === -1 || adjMat2[n * pi[i] + pi[j]] === 0)
            // Edge deletion from V1
            cost = cost + C_E * dist(adjMat1[m * i + i], adjMat1[m * j + j]);
          else
            // Edge translation
            cost =  cost +
              C_E * Math.abs(dist(adjMat1[m * i + i], adjMat1[m * j + j]) 
                - dist(adjMat2[n * pi[i] + pi[i]], adjMat2[n * pi[j] + pi[j]]));
      }
    for (let i = 0; i < n; i++)
      for (let j = i + 1; j < n; j++) {
        if (
          adjMat2[n * i + j] === 1 &&
          (!pi.includes(i) || !pi.includes(j) || 
            adjMat1[n * pi.indexOf(i) + pi.indexOf(j)] === 0)
        )
        // Edge deletion from V2
        cost = cost + C_E * dist(adjMat2[n * i + i], adjMat2[n * j + j]);
      }  
    return cost;
  }

  pi[i] = -1;
  let out = ggd(adjMat1, adjMat2, C_V, C_E, i + 1, j, pi);
  
  for(let k = 0; k < n; k++) {
    if(k === j)
      continue;
    pi[i] = k;
    const d = ggd(adjMat1, adjMat2, C_V, C_E, i + 1, k, pi);
    if(d < out)
      out = d;
  }
  return out;
}

function dist([a, b], [c, d]) {
  return Math.sqrt((a - c) * (a - c) + (b - d) * (b - d));
}

export { ggd, dist };
