import * as d3 from 'd3';

interface Node {
  hash: string;
  left?: Node;
  right?: Node;
}

const leaves: string[] = [];

const svg = d3.select('#tree')
  .append('svg')
  .attr('width', '100%')
  .attr('height', '100%');

async function sha256(message: string): Promise<string> {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function buildTree(data: string[]): Promise<Node | undefined> {
  if (data.length === 0) return undefined;
  let nodes = await Promise.all(data.map(async d => ({ hash: await sha256(d) })));
  while (nodes.length > 1) {
    const next: Node[] = [];
    for (let i = 0; i < nodes.length; i += 2) {
      const left = nodes[i];
      const right = nodes[i + 1];
      if (right) {
        const parentHash = await sha256(left.hash + right.hash);
        next.push({ hash: parentHash, left, right });
      } else {
        next.push(left);
      }
    }
    nodes = next;
  }
  return nodes[0];
}

function drawTree(root: Node | undefined) {
  svg.selectAll('*').remove();
  if (!root) return;

  const hierarchy = d3.hierarchy(root, d => [d.left, d.right].filter(Boolean) as Node[]);
  const treeLayout = d3.tree<Node>().size([400, 380]);
  const treeData = treeLayout(hierarchy);

  const g = svg.append('g').attr('transform', 'translate(20,20)');

  g.selectAll('.link')
    .data(treeData.links())
    .enter()
    .append('line')
    .attr('class', 'link')
    .attr('stroke', '#999')
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);

  const nodes = g.selectAll('.node')
    .data(treeData.descendants())
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', d => `translate(${d.x},${d.y})`);

  nodes.append('circle').attr('r', 10).attr('fill', '#69b3a2');
  nodes.append('text').attr('dy', -15).attr('text-anchor', 'middle').text(d => d.data.hash.slice(0, 6));
}

async function update() {
  const root = await buildTree(leaves);
  drawTree(root);
}

const addLeafButton = document.getElementById('addLeaf')!;
const input = document.getElementById('dataInput') as HTMLInputElement;

async function addLeaf() {
  if (input.value.trim()) {
    leaves.push(input.value.trim());
    input.value = '';
    await update();
  }
}

// Handle button click
addLeafButton.addEventListener('click', addLeaf);

// Handle Enter key press
input.addEventListener('keypress', async (e) => {
  if (e.key === 'Enter') {
    await addLeaf();
  }
});

update();
