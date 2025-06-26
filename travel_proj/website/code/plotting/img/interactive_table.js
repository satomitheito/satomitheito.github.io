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
        
        // Initialize with all columns visible
        columnDefs: [
            { targets: '_all', visible: true }
        ],
        
        // Add custom styles
        initComplete: function() {
            $('.dataTables_wrapper').addClass('custom-datatable');
        },
        
        // Add language options
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ countries",
            infoEmpty: "Showing 0 to 0 of 0 countries",
            infoFiltered: "(filtered from _MAX_ total countries)"
        }
    });
}); 