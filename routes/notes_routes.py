from flask import Blueprint,session,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import db,Note,Tag
import logging

logger = logging.getLogger(__name__)

note_bp = Blueprint('notes',__name__)

# ── CREATE NOTE ───────────────────────────────────────────────────────────────

@note_bp.route('/add_note', methods = ['POST'])
@jwt_required()
def add_note():

    user_id = int(get_jwt_identity())

    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error':'Title is required'}),400
    
    note = Note(
        title = data.get('title'),
        content = data.get('content'),
        user_id = user_id,
        is_pinned = data.get('is_pinned',False)
    )

    tag_names = data.get('tags',[])
    for name in tag_names:
        name = name.strip().lower()
        if not name:
            continue

        tag = Tag.query.filter_by(name = name, user_id=user_id).first()
        if not tag:
            tag = Tag(name=name,user_id=user_id)
            db.session.add(tag)

        note.tags.append(tag)   

    db.session.add(note)    
    db.session.commit()
    
    return jsonify({
        'message':'Note Created',
        'note':note.to_dict()
    }),201
 
# ── GET ONE NOTE ──────────────────────────────────────────────────────────────

@note_bp.route('/get_note/<int:id>',methods = ['GET'])
@jwt_required()
def get_note(id):

    user_id = get_jwt_identity()

    note = db.session.get(Note, id)

    if not note:
        return jsonify({
          'error':'Note not found'
        }),400
    
    if note.user_id != int(user_id):
        return jsonify({'error':'Unauthorized'}),403
    
    return jsonify({'note':note.to_dict()}),200

# ── GET ALL NOTES (with search + pagination) ──────────────────────────────────

@note_bp.route('/get_notes',methods = ['GET'])
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())

    print("JWT identity:", get_jwt_identity())
 
    search = request.args.get('search','')
    page = request.args.get('page',1,type=int)
    limit = request.args.get('limit',10,type=int)
    tag = request.args.get('tag','')
    pinned = request.args.get('pinned',)

    query = Note.query.filter_by(user_id=user_id)

    if search :
        query = query.filter(
           db.or_(
               Note.title.ilike(f"%{search}%"),
               Note.content.ilike(f"%{search}%"),
           )
        )
        
    if tag:
        query = query.filter(Note.tags.any(Tag.name == tag))    

    if pinned:
       if pinned.lower() == 'true':
        query = query.filter_by(is_pinned=True)  

    query = query.order_by(Note.is_pinned.desc(), Note.updated_at.desc())          

    paginated = query.paginate(page=page,per_page=limit,error_out=False)
    
    response = {
        "notes": [n.to_dict() for n in paginated.items]
    }
    logger.info(f"Get Notes Response -----> {response}")

    return jsonify({
        'notes':[n.to_dict() for n in paginated.items],
        'total':paginated.total,
        'page':paginated.page,
        'pages':paginated.pages,
        'has_next':paginated.has_next,
        'has_prev':paginated.has_prev
    }),200

# ── UPDATE NOTE ───────────────────────────────────────────────────────────────

@note_bp.route('/update_note/<int:id>',methods = ['PUT'])
@jwt_required()
def update_note(id):

    user_id = int(get_jwt_identity())
    note = db.session.get(Note, id)

    if not note:
        return jsonify({'error':'No Note Found'}),404
    if note.user_id != user_id:
        return jsonify({"error":'Unauthorized'}),403
    
    data = request.get_json()

    if not data:
        return jsonify({'error':'No data found'}),404
    
    note.title   = data.get('title',   note.title)
    note.content = data.get('content', note.content) 

    if 'tags' in data:
        note.tags = []
        for name in data['tags']:
            name = name.strip().lower()
            if not name:
                continue

            tag = Tag.query.filter_by(name=name, user_id=user_id).first()
            if not tag:
                tag = Tag(name=name, user_id=user_id)
                db.session.add(tag)

            note.tags.append(tag)   
    
    db.session.commit()

    return jsonify({
        'message':'Note Updated',
        'note':note.to_dict()
    }),200

# ── PIN / UNPIN NOTE ──────────────────────────────────────────────────────────

@note_bp.route("/<int:id>/pin", methods= ['PATCH'])
@jwt_required()
def toggle_pin(id):

    user_id = int(get_jwt_identity())

    note = db.session.get(Note, id)

    if not note:
        return jsonify({'error':'No Note Found'}),404
    if note.user_id != user_id:
        return jsonify({"error":'Unauthorized'}),403
    
    note.is_pinned = not note.is_pinned
    db.session.commit()

    status = 'Pinned' if note.is_pinned else 'Unpinned'

    return jsonify({
        'message':f"Note {status}",
        'is_pinned':note.is_pinned
    }),200
    
# ── DELETE NOTE ───────────────────────────────────────────────────────────────

@note_bp.route('/delete_note/<int:id>',methods = ['DELETE'])
@jwt_required()
def delete_note(id):

    user_id = get_jwt_identity()

    note = db.session.get(Note, id)

    if not note:
        return jsonify({
            'error':'No Note Found'
        }),404
    
    if note.user_id != int(user_id):
        return jsonify({
            'error':'Unauthorized'
        }),403
    
    db.session.delete(note)
    db.session.commit()

    return jsonify({
        'message':'Note Deleted Successfully',
    }),200