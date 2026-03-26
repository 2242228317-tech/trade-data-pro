const fs = require('fs');
const path = require('path');

// Simple function to write file with UTF-8 encoding
function writeFile(filePath, content) {
  fs.writeFileSync(filePath, content, { encoding: 'utf8' });
  console.log(`Written: ${filePath}`);
}

// Create directories if needed
const dirs = [
  'app/analytics',
  'app/customs', 
  'app/tools/product-research'
];

dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

console.log('Creating stub files...');
writeFile('app/analytics/page.tsx', `export default function AnalyticsPage() { return <div>Analytics</div>; }`);
writeFile('app/customs/page.tsx', `export default function CustomsPage() { return <div>Customs</div>; }`);
writeFile('app/tools/product-research/page.tsx', `export default function ProductResearchPage() { return <div>Product Research</div>; }`);

console.log('Done!');
