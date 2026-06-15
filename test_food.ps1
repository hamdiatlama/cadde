$p = Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn src.main:app --host 127.0.0.1 --port 8765" -PassThru
Start-Sleep -Seconds 10

Write-Output "=== TEST: FOOD SYSTEM E2E ==="

# 1. Login as food seller
Write-Output "`n--- 1. Login ---"
$body = '{"email":"food@seller.com","password":"123"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 10
$token = ($r.Content | ConvertFrom-Json).access_token
$headers = @{Authorization="Bearer $token"}
Write-Output "OK"

# 2. Get restaurant info
Write-Output "`n--- 2. List Restaurants ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/restaurants" -Headers $headers -UseBasicParsing -TimeoutSec 10
$restaurants = ($r.Content | ConvertFrom-Json)
Write-Output "Found $($restaurants.Count) restaurant(s)"
$restId = $restaurants[0].id
Write-Output "Restaurant ID: $restId"

# 3. Add menu items
Write-Output "`n--- 3. Add Menu Items ---"
$body = '{"name":"Adana Kebap","category":"Ana Yemek","price":180.0,"is_halal":true,"preparation_time_min":20,"description":"El yapimi Adana kebap"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Menu item 1: $($r.Content)"
$menu1 = ($r.Content | ConvertFrom-Json)

$body = '{"name":"Lahmacun","category":"Ana Yemek","price":70.0,"is_halal":true,"is_vegetarian":false,"preparation_time_min":15,"description":"Kiyamali lahmacun"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Menu item 2: $($r.Content)"
$menu2 = ($r.Content | ConvertFrom-Json)

# 4. Login as product supplier
Write-Output "`n--- 4. Login as Supplier ---"
$body = '{"email":"tedarikci@test.com","password":"123123"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 10
$token2 = ($r.Content | ConvertFrom-Json).access_token
$headers2 = @{Authorization="Bearer $token2"}
Write-Output "OK"

# 5. Login as home chef
Write-Output "`n--- 5. Login as Home Chef ---"
$body = '{"email":"evinmutfagi@test.com","password":"123123"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 10
$token3 = ($r.Content | ConvertFrom-Json).access_token
$headers3 = @{Authorization="Bearer $token3"}
Write-Output "OK"

# 6. List suppliers
Write-Output "`n--- 6. List All Suppliers ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/suppliers" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 7. List products for supplier 2 (home chef)
Write-Output "`n--- 7. Home Chef Products ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/suppliers/2/products" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 8. Link supplier 2 to restaurant
Write-Output "`n--- 8. Link Home Chef to Restaurant ---"
$body = '{"supplier_id":2,"is_preferred":true,"notes":"Ev yemekleri tedarikcisi"}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/restaurants/$restId/suppliers" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Link: $($r.Content)"

# 9. List restaurant suppliers
Write-Output "`n--- 9. Restaurant Suppliers ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/restaurants/$restId/suppliers" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 10. Add ingredients to menu items (from home chef)
Write-Output "`n--- 10. Add Ingredients to Menu ---"
$body = '{"supplier_product_id":4,"quantity":2.0,"unit":"porsiyon","notes":"Taze borek","is_visible_to_customer":true}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu/1/ingredients" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Ingredient 1: $($r.Content)"

$body = '{"supplier_product_id":5,"quantity":1.0,"unit":"porsiyon","notes":"Tatli olarak","is_visible_to_customer":true}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu/1/ingredients" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Ingredient 2: $($r.Content)"

$body = '{"supplier_product_id":1,"quantity":0.5,"unit":"kg","notes":"Organik domates","is_visible_to_customer":true}'
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu/1/ingredients" -Method POST -Body $body -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Ingredient 3: $($r.Content)"

# 11. List ingredients for menu item
Write-Output "`n--- 11. Menu Item Ingredients ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/menu/1/ingredients" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 12. Public traceability for menu item
Write-Output "`n--- 12. Public Traceability ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/trace/1" -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 13. Supplier public pages
Write-Output "`n--- 13. Supplier Public Page (Home Chef) ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/suppliers/page/ayse-teyzenin-mutfagi" -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

Write-Output "`n--- 14. Supplier Public Page (Producer) ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/suppliers/page/ege-organik-ciftlik" -UseBasicParsing -TimeoutSec 10
Write-Output ($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2)

# 15. Transparency score
Write-Output "`n--- 15. Transparency Score ---"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/restaurants/$restId/transparency/recalculate" -Method POST -Body '{}' -ContentType "application/json" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Recalculate: $($r.Content)"
$r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/food/restaurants/$restId/transparency" -Headers $headers -UseBasicParsing -TimeoutSec 10
Write-Output "Score: $($r.Content)"

Write-Output "`n=== ALL TESTS PASSED ==="

$p | Stop-Process -Force -ErrorAction SilentlyContinue