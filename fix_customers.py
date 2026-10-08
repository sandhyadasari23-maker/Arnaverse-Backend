import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Customers.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            } else {
                container.innerHTML = `<p style="color:red">Failed to load customers.</p>`;
            }
        } catch (err) {
            console.error(err);
            container.innerHTML = `<p style="color:red">Error loading customers.</p>`;
        }
    };'''

replacement = '''            } else {
                if (!cachedCustomers) {
                    container.innerHTML = `<p style="color:red">Failed to load customers: ${data.message || 'Unknown error'}</p>`;
                } else {
                    console.error("Failed to refresh customers:", data.message);
                }
            }
        } catch (err) {
            console.error(err);
            if (!cachedCustomers) {
                container.innerHTML = `<p style="color:red">Error loading customers.</p>`;
            }
        }
    };'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed Customers.js error handling")
else:
    print("Could not find target in Customers.js")
