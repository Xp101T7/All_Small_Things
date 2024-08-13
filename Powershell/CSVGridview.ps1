# Load CSV Data
$data = Import-Csv -Path "C:\path_to_your_file.csv"

# Check if data is loaded
if ($data.Count -eq 0) {
    Write-Host "No data loaded from the CSV file."
    exit
}

# Output data to console for validation
Write-Host "Data loaded from CSV:"
$data | Format-Table -Wrap -AutoSize

# Create a Windows Form
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$form = New-Object System.Windows.Forms.Form
$form.Text = "CSV Data Dashboard"
$form.Size = New-Object System.Drawing.Size(800, 600)

# Create a DataGridView to display the data
$datagridview = New-Object System.Windows.Forms.DataGridView
$datagridview.Size = New-Object System.Drawing.Size(780, 560)
$datagridview.Location = New-Object System.Drawing.Point(10, 10)
$datagridview.AutoGenerateColumns = $true

# Convert CSV data to DataTable
$datatable = New-Object System.Data.DataTable
$data[0].PSObject.Properties.Name | ForEach-Object {
    try {
        $column = $datatable.Columns.Add($_.ToString()) #* Convert column name to string
        $column.AllowDBNull = $true #* Allow null values in the column
    }
    catch {
        Write-Host "Error adding column '$_': $($_.Exception.Message)" #* Display error message
    }
}

$data | ForEach-Object {
    $row = $datatable.NewRow()
    $_.PSObject.Properties | ForEach-Object {
        try {
            $value = $_.Value
            if ($value -eq $null -or $value -is [System.DBNull]) { #* Check for null or DBNull
                $row[$_.Name] = [System.DBNull]::Value #* Set value as DBNull
            }
            else {
                $row[$_.Name] = $value
            }
        }
        catch {
            Write-Host "Error setting value for column '$($_.Name)': $($_.Exception.Message)" #* Display error message
        }
    }
    $datatable.Rows.Add($row)
}

# Debug statements to check DataTable population
Write-Host "Number of rows in DataTable: $($datatable.Rows.Count)"
Write-Host "DataTable content:"
$datatable | Format-Table -AutoSize

# Bind the DataTable to the DataGridView
$datagridview.DataSource = $datatable

# Add the DataGridView to the form
$form.Controls.Add($datagridview)

# Show the form
$form.Add_Shown({ $form.Activate() })
$form.ShowDialog()