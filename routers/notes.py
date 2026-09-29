from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Note
from schemas import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note and save it to your database"""
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    # reload the note so it includes the id and created_at the database generated
    db.refresh(db_note)
    return db_note


@router.get("", response_model=list[NoteResponse])
def list_notes(
    category: str | None = None,
    is_pinned: bool | None = None,
    db: Session = Depends(get_db),
):
    """List all notes, optionally filtered by the category and/or pinned"""
    # will only apply filters if the user specifically states them 
    # "is not None" (not just "if is_pinned") so is_pinned=false still filters
    query = db.query(Note)
    if category is not None:
        query = query.filter(Note.category == category)
    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)
    return query.all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a single note by looking up its id. Return 404 if it doesn't exist"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note by its id and return 404 if it doesn't exist"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    # HTTP code 204! NO CONTENT! Successful but nothing to return.