from flask import Blueprint,session,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import db,Note


note_bp = Blueprint('notes',__name__)

@note_bp.route('/add_note', methods = ['POST'])
@jwt_required()
def add_note():

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({
            'error':'No Data Found'
        }),404
    
    title = data.get('title','').strip()

    if not title:
        return jsonify({
            'error': 'Title is required'
        }), 400

    if len(title) > 100:                     # validate title length
        return jsonify({
            'error': 'Title must be under 100 characters'
        }), 400
    
    content = data.get('content', '').strip()  # content is optional, default empty string

    if len(content) > 500:                   # validate content length
        return jsonify({
            'error': 'Content must be under 500 characters'
        }), 400
    
    note = Note(title=title,content=content,user_id=int(user_id))

    db.session.add(note)
    db.session.commit()

    return jsonify({
        'message': 'Note added successfully',
        'note': note.to_dict()
    }),201

@note_bp.route('/get_note/<int:id>',methods = ['GET'])
@jwt_required()
def get_note(id):

    user_id = get_jwt_identity()

    note = db.session.get(Note,id)

    if not note:
        return jsonify({
            'error':'No Note Found'
        }),404
    
    if note.user_id != user_id:
        return jsonify({
            'error':'Unauthorized'
        }),403
    
    return jsonify({
        'note':note.to_dict()
    }),200

@note_bp.route('/get_notes',methods = ['GET'])
@jwt_required()
def get_notes():

    user_id = get_jwt_identity()

# pagination params
    page = request.args.get('page',1,type=int)  #Read page from query params
    per_page = request.args.get('per_page',10 , type=int) #Read per_page

# search params
    search = request.args.get('search','',type=str).strip()

# base query   
    notes_query = Note.query.filter_by(user_id=int(user_id))

 # apply search if exists
    if search:
        notes_query = notes_query.filter(
            #ilike - case-insensitive
            #like - case-sensitive
            Note.title.ilike(f"%{search}%") |
            Note.content.ilike(f"%{search}%")
        )
    pagination = notes_query.paginate(page=page,per_page=per_page,error_out=False)

    if not pagination.items:
        return jsonify({
            'error':'No Notes Found'
        }),404
    
    return jsonify({
        'notes':[n.to_dict() for n in pagination.items],  #current page data
        'total':pagination.total,  #total rows in DB
        'page':pagination.page,
        'pages':pagination.pages,
        'per_page':pagination.per_page,
        'search': search
    }),200

@note_bp.route('/update_note/<int:id>',methods = ['PUT'])
@jwt_required()
def update_note(id):

    user_id = get_jwt_identity()
    note = db.session.get(Note,id)
 
    if not note:
        return jsonify({
            'error':'No Notes Found'
        }),404
    if note.user_id != user_id:
        return jsonify({
            'error':'Unauthorized'
        }),403
    
    data = request.get_json()
    if not data:
        return jsonify({
            'error':'No data provided'
        }),400
     
    if 'title' in data:
        title = data.get('title','')
        if not title:
            return jsonify({'error': 'Title cannot be empty'}), 400
        if len(title) > 100:
            return jsonify({'error': 'Title must be under 100 characters'}), 400
        note.title = title

    if 'content' in data:
        content = data['content'].strip()
        if len(content) > 500:
            return jsonify({'error': 'Content must be under 500 characters'}), 400
        note.content = content 

    db.session.commit()       

    return jsonify({
        'message': 'Note updated successfully',
        'note': note.to_dict()
    }), 200

@note_bp.route('/delete_note/<int:id>',methods = ['DELETE'])
@jwt_required()
def delete_note(id):

    user_id = get_jwt_identity()

    note = db.session.get(Note, id)

    if not note:
        return jsonify({
            'error':'No Note Found'
        }),404
    
    if note.user_id != user_id:
        return jsonify({
            'error':'Unauthorized'
        }),403
    
    db.session.delete(note)
    db.session.commit()

    return jsonify({
        'message':'Note Deleted Successfully',
    }),200