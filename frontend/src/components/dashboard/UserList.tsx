import React from 'react';
import { UserProfile } from '../../types';

interface Props { users: UserProfile[]; silentUsers: UserProfile[]; }
export default function UserList({ users, silentUsers }: Props) {
  return <div></div>;
}
