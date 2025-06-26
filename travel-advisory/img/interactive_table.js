// Initialize DataTables when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the DataTables plugin on our table with ID 'travel-advisory-table'
    $('#travel-advisory-table').DataTable({
        // Enable responsive design for mobile/tablet viewing
        responsive: true,
        
        // Set pagination options
        paging: true,
        pageLength: 15,
        lengthMenu: [[10, 15, 25, 50, -1], [10, 15, 25, 50, "All"]],
        
        // Enable column-wise filtering
        searching: true,
        
        // Enable sorting
        ordering: true,
        
        // Setup default sorting (Country name, ascending)
        order: [[0, 'asc']],
        
        // Add fixed header that stays visible when scrolling
        fixedHeader: true,
        
        // Add buttons for export options
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        
        // Configure columns to better handle different data types and widths
        columnDefs: [
            { targets: '_all', visible: true },
            { targets: 0, width: '15%' }, // Country
            { targets: 1, width: '18%' }, // Advisory Level
            { targets: 2, width: '9%' }, // Date Updated
            { targets: 3, width: '7%', className: 'dt-right' }, // GPI Score
            { targets: 4, width: '7%', className: 'dt-right' }, // GTI Score
            { targets: 5, width: '12%', className: 'dt-right' }, // Tourist Arrivals
            { targets: 6, width: '10%', className: 'dt-right', priority: 1 } // Number of Deaths - higher priority
        ],
        
        // Add custom styles
        initComplete: function() {
            $('.dataTables_wrapper').addClass('custom-datatable');
            
            // Force redraw to ensure all columns are visible
            $(window).trigger('resize');
        },
        
        // Add language options
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ countries",
            infoEmpty: "Showing 0 to 0 of 0 countries",
            infoFiltered: "(filtered from _MAX_ total countries)"
        },
        
        // Ensure horizontal scrolling is enabled
        scrollX: true,
        scrollCollapse: true,
        
        // Ensure full width is used
        autoWidth: false
    });
}); 