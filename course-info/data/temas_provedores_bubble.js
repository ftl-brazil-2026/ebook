(function () {
  const colors = { 
    br: "#10b981",
    gl: "#ec4899",
    catBg: "#1A2A4F",
    catBorder: "#2F3C7E",
    textMain: "#F2E8C9",
    textDark: "#0B1026"
  };
  
  const W = 900, H = 800;
  const svg = d3.select("#geoSvg").attr("viewBox", [0, 0, W, H]);
  const zoomGroup = svg.append("g");
  const panel = d3.select("#geoPanel");
  const tooltip = d3.select("#tooltip");

  d3.json("provedores.json").then(DATA => {
    const root = d3.hierarchy({
      name: "root",
      children: DATA.categorias.map(c => ({
        name: c.nome, votos: c.votos,
        children: c.provedores.map(p => ({ name: p.nome, escopo: p.escopo, url: p.url, dado: p.dado, value: 1 }))
      }))
    })
    .sum(d => d.value)
    .sort((a, b) => (b.data.votos || 0) - (a.data.votos || 0));

    root.children.forEach(c => { c.value = 6 + (c.data.votos || 1) * 3; });
    root.value = d3.sum(root.children, c => c.value);

    d3.pack().size([W, H]).padding(d => d.depth === 0 ? 30 : 6)(root);

    let focus = root, view;

    const nodesLayer = zoomGroup.append("g");
    const labelsLayer = zoomGroup.append("g");

    const nodePosition = nodesLayer.selectAll("g.node-pos")
      .data(root.descendants().slice(1))
      .join("g")
      .attr("class", "node-pos")
      .attr("transform", d => `translate(${d.x},${d.y})`);

    const nodeFloat = nodePosition.append("g")
      .attr("class", "node-float")
      .style("animation", d => `floatBubble ${3 + (d.x % 3)}s ease-in-out infinite alternate`)
      .style("animation-delay", d => `-${d.y % 4}s`);

    const circles = nodeFloat.append("circle")
      .attr("r", d => d.r)
      .attr("fill", d => d.depth === 1 ? colors.catBg : (d.data.escopo === "BR" ? colors.br : colors.gl))
      .attr("stroke", d => d.depth === 1 ? colors.catBorder : "none")
      .attr("stroke-width", d => d.depth === 1 ? 1 : 0)
      .style("opacity", d => d.depth === 2 ? 0.3 : 1) 
      .style("pointer-events", d => d.depth === 2 ? "none" : "auto")
      .on("mouseover", function (event, d) {
        if (d.depth === 1) {
          d3.select(this).attr("stroke", colors.textMain).attr("stroke-width", 3);
        } else if (d.depth === 2) {
          d3.select(this).attr("stroke", "#ffffff").attr("stroke-width", 2);
          tooltip.style("opacity", 1)
            .html(`<strong style="color:${d.data.escopo === 'BR' ? colors.br : colors.gl}">${d.data.name}</strong><br/><span style="color:#A9B6FF; font-size:11.5px; margin-top:4px; display:block;">Clique para acessar</span>`)
            .style("left", (event.pageX + 15) + "px").style("top", (event.pageY - 30) + "px");
        }
      })
      .on("mousemove", event => tooltip.style("left", (event.pageX + 15) + "px").style("top", (event.pageY - 30) + "px"))
      .on("mouseout", function (event, d) {
        if (d.depth === 1) {
          d3.select(this).attr("stroke", colors.catBorder).attr("stroke-width", 1);
        } else if (d.depth === 2) {
          d3.select(this).attr("stroke-width", 0);
        }
        tooltip.style("opacity", 0);
      })
      .on("click", (event, d) => {
        event.stopPropagation();
        if (d.depth === 1) { zoomToNode(d); showCategory(d); }
        else { showProvider(d); window.open(d.data.url, "_blank", "noopener"); }
      });

    const labelPosition = labelsLayer.selectAll("g.label-pos")
      .data(root.descendants().slice(1))
      .join("g")
      .attr("class", "label-pos")
      .attr("transform", d => `translate(${d.x},${d.y})`);

    const labelFloat = labelPosition.append("g")
      .attr("class", "label-float")
      .style("animation", d => `floatBubble ${3 + (d.x % 3)}s ease-in-out infinite alternate`)
      .style("animation-delay", d => `-${d.y % 4}s`);

    const labelCat = labelFloat.filter(d => d.depth === 1).append("text")
      .attr("text-anchor", "middle")
      .style("fill", colors.textMain)
      .style("stroke", colors.textDark)
      .style("stroke-width", d => (d.r * 0.08) + "px") 
      .style("paint-order", "stroke fill")
      .style("font-size", d => (d.r * 0.28) + "px") 
      .style("font-weight", "800")
      .style("pointer-events", "none")
      .each(function (d) { wrapText(d3.select(this), d.data.name, d.r * 1.6); });

    const labelProv = labelFloat.filter(d => d.depth === 2).append("text")
      .attr("text-anchor", "middle")
      .style("fill", "#ffffff")
      .style("stroke", colors.textDark)
      .style("stroke-width", d => (d.r * 0.08) + "px") 
      .style("paint-order", "stroke fill")
      .style("font-size", d => (d.r * 0.28) + "px") 
      .style("font-weight", "800")
      .style("pointer-events", "none")
      .style("opacity", 0) 
      .each(function (d) { wrapText(d3.select(this), d.data.name, d.r * 1.6); });

    const zoomBehavior = d3.zoom()
      .scaleExtent([0.8, 10])
      .on("zoom", (event) => {
        zoomGroup.attr("transform", event.transform);
        circles.filter(c => c.depth === 2).style("pointer-events", event.transform.k > 2 ? "auto" : "none");
      });

    svg.call(zoomBehavior);
    svg.on("click", () => { zoomToNode(root); panel.html(intro()); });
    
    zoomToNode(root, 0);
    panel.html(intro());
    reportHeight();

    function zoomToNode(d, duration = 850) {
      focus = d;
      const padding = d.depth === 0 ? 20 : 60;
      const k = d.depth === 0 ? 1 : Math.min(8, (W - padding) / (d.r * 2));
      const x = W / 2 - d.x * k;
      const y = H / 2 - d.y * k;

      const transition = svg.transition().duration(duration).ease(d3.easeCubicOut);
      svg.transition(transition).call(zoomBehavior.transform, d3.zoomIdentity.translate(x, y).scale(k));

      labelCat.transition(transition).style("opacity", l => focus === root ? 1 : 0);
      labelProv.transition(transition).style("opacity", l => l.parent === focus ? 1 : 0);

      circles.filter(c => c.depth === 2).transition(transition)
        .style("opacity", c => c.parent === focus ? 1 : (focus === root ? 0.3 : 0));
    }

    function wrapText(textSelection, textString, maxWidth) {
      if (!textString) return;
      const words = textString.split(/\s+/).reverse();
      let word, line = [], lineHeight = 1.1;
      let tspan = textSelection.text(null).append("tspan").attr("x", 0).attr("dy", "0em");
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > maxWidth && line.length > 1) {
          line.pop(); tspan.text(line.join(" ")); line = [word];
          tspan = textSelection.append("tspan").attr("x", 0).attr("dy", lineHeight + "em").text(word);
        }
      }
      const numLines = textSelection.selectAll("tspan").size();
      const dy0 = -(numLines - 1) * lineHeight / 2;
      textSelection.selectAll("tspan").attr("dy", (d, i) => (i === 0 ? dy0 : lineHeight) + "em");
    }

    function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

    function intro() {
      const nCat = DATA.categorias.length;
      const nProv = new Set(DATA.categorias.flatMap(c => c.provedores.map(p => p.nome))).size;
      return `<div class="geo-panel-header"><h3 class="geo-panel-title">${esc(DATA.meta.titulo)}</h3><div class="geo-panel-meta">${nCat} Temas &middot; ${nProv} Provedores</div></div>`;
    }

    function showCategory(d) {
      const c = DATA.categorias.find(x => x.nome === d.data.name);
      const items = c.provedores.map(p => `
        <li class="${p.escopo === 'BR' ? 'br' : 'gl'}">
          <span class="pill">${p.escopo === 'BR' ? 'BR' : 'GLOBAL'}</span>
          <a href="${p.url}" target="_blank" rel="noopener">${esc(p.nome)}</a>
          <span class="desc">${esc(p.dado)}</span>
        </li>`).join("");
      
      panel.html(`<div class="geo-panel-header"><h3 class="geo-panel-title">${esc(c.nome)}</h3><div class="geo-panel-meta">${c.provedores.length} provedores mapeados neste tema</div></div><ul class="geo-list">${items}</ul>`);
      reportHeight();
    }

    function showProvider(d) {
      panel.html(`<div class="geo-panel-header"><h3 class="geo-panel-title"><a href="${d.data.url}" target="_blank" rel="noopener">${esc(d.data.name)}</a></h3><div class="geo-panel-meta">${d.data.escopo === 'BR' ? 'Nacional' : 'Global'} &middot; Tema: ${esc(d.parent.data.name)}</div></div><ul class="geo-list" style="grid-template-columns: 1fr;"><li class="${d.data.escopo === 'BR' ? 'br' : 'gl'}"><span class="pill">${d.data.escopo === 'BR' ? 'BR' : 'GLOBAL'}</span><span class="desc">${esc(d.data.dado)}</span></li></ul>`);
      reportHeight();
    }

  }).catch(err => {
    panel.html(`<p style="color:#ef4444; text-align:center;">Erro de sistema: ${err}</p>`);
    reportHeight();
  });

  function reportHeight() {
    requestAnimationFrame(() => window.parent.postMessage({ type: "geo-resize", height: document.documentElement.scrollHeight }, "*"));
  }
  window.addEventListener("resize", reportHeight);
})();