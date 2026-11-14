<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TodoController;

// API Route untuk menambahkan Todo
Route::post('/api/todos', [TodoController::class, 'store']);

// API Route untuk menampilkan semua Todo
Route::get('/api/todos', [TodoController::class, 'index']);
	Route::delete('/api/todos/{todo}', [TodoController::class, 'destroy']);

// API Route untuk update Todo
Route::put('/api/todos/{todo}', [TodoController::class, 'update']);
