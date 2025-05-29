# Change to project root
Set-Location "C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup"

# Create folders
$folders = @(
  "components",
  "layouts",
  "types",
  "styles",
  "pages/admin/channel",
  "public/images",
  "data"
)

foreach ($folder in $folders) {
  if (-Not (Test-Path $folder)) {
    New-Item -ItemType Directory -Path $folder
  }
}

# Create placeholder files
$files = @{
  "pages/index.tsx" = "// TODO: Homepage"
  "pages/explore.tsx" = "// TODO: Explore Page"
  "pages/player/[id].tsx" = "// TODO: Podcast Player Page"
  "pages/admin/index.tsx" = "// TODO: Admin Login"
  "pages/admin/dashboard.tsx" = "// TODO: Admin Dashboard"
  "pages/admin/feeds.tsx" = "// TODO: Feed Manager"
  "pages/admin/channel/[id].tsx" = "// TODO: Channel Detail"
  "components/Sidebar.tsx" = "// TODO: Sidebar Component"
  "components/PodcastCard.tsx" = "// TODO: Podcast Card"
  "layouts/DashboardLayout.tsx" = "// TODO: Admin Layout"
  "types/index.ts" = "// TODO: Shared types"
  "styles/globals.css" = "/* TODO: Tailwind base styles */"
}

foreach ($file in $files.Keys) {
  $fullPath = Join-Path $PWD $file
  if (-Not (Test-Path $fullPath)) {
    New-Item -ItemType File -Path $fullPath -Force | Out-Null
    Set-Content -Path $fullPath -Value $files[$file]
  }
}

Write-Host "✅ Podverse project structure initialized!" -ForegroundColor Green
